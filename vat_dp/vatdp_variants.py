
import datetime
import glob
import hashlib
import json
import os
import random
import re

import pysam
import google.protobuf.struct_pb2 as struct_pb2

# import ga4gh.protocol as protocol
# import ga4gh.exceptions as exceptions
import datamodel as datamodel
# import ga4gh.pb as pb



def isUnspecified(str):
    """
    Checks whether a string is None or an
    empty string. Returns a boolean.
    """
    return str == "" or str is None


class CallSet():
    """
    Class representing a CallSet. A CallSet basically represents the
    metadata associated with a single VCF sample column.
    """

    def __init__(self):
        self._sampleName = None


    def setSampleName(self, sampleName):
        """
        Set the bioSampleId for the current sample.
        """
        self._sampleName = sampleName

    def getSampleName(self):
        """
        Returns the sample name for this CallSet.
        """
        return self._sampleName



class AbstractVariantSet():
    """
    An abstract base class of a variant set
    """


    def __init__(self):
        self._callSetNameMap = {}
        self._metadata = []
    

    def addCallSet(self, callSet):
        """
        Adds the specfied CallSet to this VariantSet.
        """
        self._callSetNameMap[callSet.getSampleName()] = callSet


    def addCallSetFromName(self, sampleName):
        """
        Adds a CallSet for the specified sample name.
        """
        callSet = CallSet(self, sampleName)
        self.addCallSet(callSet)

    def getCallSets(self):
        """
        Returns the list of CallSets in this VariantSet.
        """
        return [self._callSetNameMap[sampleName] for sampleName in self._callSetNameMap]


     def getNumCallSets(self):
    #     """
    #     Returns the number of CallSets in this variant set.
    #     """
          return len(_callSetNameMap)

    def getCallSetByName(self, sampleName):
        """
        Returns a CallSet with the specified name, or raises a
        CallSetNameNotFoundException if it does not exist.
        """
        # if name not in self._callSetNameMap:
        #     raise exceptions.CallSetNameNotFoundException(name)
        return self._callSetNameMap[smapleName]


    def getMetadata(self):
        """
        Returns Metdata associated with this VariantSet
        """
        return self._metadata


    def getNumVariants(self):
    #     """
    #     Returns the number of variants contained in this VariantSet.
    #     """
         raise NotImplementedError()



    def getVariantId(self, gaVariant):
        """
        Returns an ID string suitable for the specified GA Variant
        object in this variant set.
        """
        ##implement chr,pos,ref,alt to id
        variantID="" 
        return variantID




class ESVariantSet(AbstractVariantSet):
    """
    Class representing a single variant set backed by a directory of indexed
    VCF or BCF files.
    """
    def __init__(self):
        self._chromFileMap = {}
        self._metadata = None


    def getReferenceToDataIndexMap(self):
        """
        Returns the map of Reference names to the (dataUrl, indexFile) pairs.
        """
        return self._chromFileMap

    def getDataIndexPairs(self):
        """
        Returns the set of (dataUrl, indexFile) pairs.
        """
        return set(self._chromFileMap.values())



    def populateFromFile(self, dataFiles, indexFiles):
        """
        Populates this variant set using the specified lists of data
        files and indexes. These must be in the same order, such that
        the jth index file corresponds to the jth data file.
        """
        assert len(dataFiles) == len(indexFiles)
        for dataFile, indexFile in zip(dataFiles, indexFiles):
            varFile = pysam.VariantFile(dataUrl, index_filename=indexFile)
            try:
                self._populateFromVariantFile(varFile, dataFile, indexFile)
            finally:
                varFile.close()

    def populateFromDirectory(self, vcfDirectory):
        """
        Populates this VariantSet by examing all the VCF files in the
        specified directory. This is mainly used for as a convenience
        for testing purposes.
        """
        pattern = os.path.join(vcfDirectory, "*.vcf.gz")
        dataFiles = []
        indexFiles = []
        for vcfFile in glob.glob(pattern):
            dataFiles.append(vcfFile)
            indexFiles.append(vcfFile + ".tbi")
        self.populateFromFile(dataFiles, indexFiles)

    def getVcfHeaderReferenceSetName(self):
        """
        Returns the name of the reference set from the VCF header.
        """
        # TODO implemenent
        return None


    def _populateFromVariantFile(self, varFile, dataFile, indexFile):
        """
        Populates the instance variables of this VariantSet from the specified
        pysam VariantFile object.
        """
        if varFile.index is None:
            raise exceptions.NotIndexedException(dataUrl)
        for chrom in varFile.index:
            # chrom, _, _ = self.sanitizeVariantFileFetch(chrom)
            # if not isEmptyIter(varFile.fetch(chrom)):
            #     if chrom in self._chromFileMap:
            #         raise exceptions.OverlappingVcfException(dataUrl, chrom)
            self._chromFileMap[chrom] = dataFile, indexFile
        self._updateMetadata(varFile)
        self._updateCallSetIds(varFile)


   

    def _updateMetadata(self, variantFile):
        """
        Updates the metadata for his variant set based on the specified
        variant file
        """
        metadata = self._getMetadataFromVcf(variantFile)
        if self._metadata is None:
            self._metadata = metadata

    def _checkMetadata(self, variantFile):
        """
        Checks that metadata is consistent
        """
        metadata = self._getMetadataFromVcf(variantFile)
        if self._metadata is not None and self._metadata != metadata:
            raise exceptions.InconsistentMetaDataException(
                variantFile.filename)

    def _checkCallSetIds(self, variantFile):
        """
        Checks callSetIds for consistency
        """
        if len(self._callSetIdMap) > 0:
            callSetIds = set([
                self.getCallSetId(sample)
                for sample in variantFile.header.samples])
            if callSetIds != set(self._callSetIdMap.keys()):
                raise exceptions.InconsistentCallSetIdException(
                    variantFile.filename)

    def getNumVariants(self):
        """
        Returns the total number of variants in this VariantSet.
        """
        # TODO How do we get the number of records in a VariantFile?
        return 0

    def _updateCallSetIds(self, variantFile):
        """
        Updates the call set IDs based on the specified variant file.
        """
        if len(self._callSetIdMap) == 0:
            for sample in variantFile.header.samples:
                self.addCallSetFromName(sample)

    def openFile(self, dataFileIndexFilePair):
        dataFile, indexFile = dataFileIndexFilePair
        return pysam.VariantFile(dataFile, index_filename=indexFile)

    def _convertGaCall(self, callSet, pysamCall):
        phaseset = None
        if pysamCall.phased:
            phaseset = str(pysamCall.phased)
        genotypeLikelihood = []
        info = {}
        for key, value in pysamCall.iteritems():
            if key == 'GL' and value is not None:
                genotypeLikelihood = list(value)
            elif key != 'GT':
                info[key] = _encodeValue(value)
        call = protocol.Call()
        call.call_set_name = callSet.getSampleName()
        call.call_set_id = callSet.getId()
        call.genotype.extend(list(pysamCall.allele_indices))
        call.phaseset = pb.string(phaseset)
        call.genotype_likelihood.extend(genotypeLikelihood)
        for key in info:
            call.info[key].values.extend(info[key])
        return call

    def convertVariant(self, record, callSetIds):
        """
        Converts the specified pysam variant record into a GA4GH Variant
        object. Only calls for the specified list of callSetIds will
        be included.
        """
        variant = self._createGaVariant()
        variant.reference_name = record.contig
        if record.id is not None:
            variant.names.extend(record.id.split(';'))
        variant.start = record.start          # 0-based inclusive
        variant.end = record.stop             # 0-based exclusive
        variant.reference_bases = record.ref
        if record.alts is not None:
            variant.alternate_bases.extend(list(record.alts))
        # record.filter and record.qual are also available, when supported
        # by GAVariant.
        for key, value in record.info.iteritems():
            if value is not None:
                if isinstance(value, str):
                    value = value.split(',')
                variant.info[key].values.extend(_encodeValue(value))
        for callSetId in callSetIds:
            callSet = self.getCallSet(callSetId)
            pysamCall = record.samples[str(callSet.getSampleName())]
            variant.calls.add().CopyFrom(
                self._convertGaCall(callSet, pysamCall))
        variant.id = self.getVariantId(variant)
        return variant

    def getVariant(self, compoundId):
        if compoundId.reference_name in self._chromFileMap:
            varFileName = self._chromFileMap[compoundId.reference_name]
        else:
            raise exceptions.ObjectNotFoundException(compoundId)
        start = int(compoundId.start)
        referenceName, startPosition, endPosition = \
            self.sanitizeVariantFileFetch(
                compoundId.reference_name, start, start + 1)
        cursor = self.getFileHandle(varFileName).fetch(
            referenceName, startPosition, endPosition)
        for record in cursor:
            variant = self.convertVariant(record, self._callSetIds)
            if (record.start == start and
                    compoundId.md5 == self.hashVariant(variant)):
                return variant
            elif record.start > start:
                raise exceptions.ObjectNotFoundException()
        raise exceptions.ObjectNotFoundException(compoundId)

    def getPysamVariants(self, referenceName, startPosition, endPosition):
        """
        Returns an iterator over the pysam VCF records corresponding to the
        specified query.
        """
        if referenceName in self._chromFileMap:
            varFileName = self._chromFileMap[referenceName]
            referenceName, startPosition, endPosition = \
                self.sanitizeVariantFileFetch(
                    referenceName, startPosition, endPosition)
            cursor = self.getFileHandle(varFileName).fetch(
                referenceName, startPosition, endPosition)
            for record in cursor:
                yield record

    def getVariants(self, referenceName, startPosition, endPosition,
                    callSetIds=[]):
        """
        Returns an iterator over the specified variants. The parameters
        correspond to the attributes of a GASearchVariantsRequest object.
        """
        if callSetIds is None:
            callSetIds = self._callSetIds
        else:
            for callSetId in callSetIds:
                if callSetId not in self._callSetIds:
                    raise exceptions.CallSetNotInVariantSetException(
                        callSetId, self.getId())
        for record in self.getPysamVariants(
                referenceName, startPosition, endPosition):
            yield self.convertVariant(record, callSetIds)

    def getMetadataId(self, metadata):
        """
        Returns the id of a metadata
        """
        return str(datamodel.VariantSetMetadataCompoundId(
            self.getCompoundId(), 'metadata:' + metadata.key))

    def _getMetadataFromVcf(self, varFile):
        # All the metadata is available via each varFile.header, including:
        #    records: header records
        #    version: VCF version
        #    samples -- not immediately needed
        #    contigs -- not immediately needed
        #    filters -- not immediately needed
        #    info
        #    formats

        def buildMetadata(
                key, type_="String", number="1", value="", id_="",
                description=""):  # All input are strings
            metadata = protocol.VariantSetMetadata()
            metadata.key = key
            metadata.value = value
            metadata.type = type_
            metadata.number = number
            metadata.description = description
            if id_ == '':
                id_ = self.getMetadataId(metadata)
            metadata.id = id_
            return metadata

        ret = []
        header = varFile.header
        ret.append(buildMetadata(key="version", value=header.version))
        formats = header.formats.items()
        infos = header.info.items()
        # TODO: currently ALT field is not implemented through pysam
        # NOTE: contigs field is different between vcf files,
        # so it's not included in metadata
        # NOTE: filters in not included in metadata unless needed
        for prefix, content in [("FORMAT", formats), ("INFO", infos)]:
            for contentKey, value in content:
                description = value.description.strip('"')
                key = "{0}.{1}".format(prefix, value.name)
                if key != "FORMAT.GT":
                    ret.append(buildMetadata(
                        key=key, type_=value.type,
                        number="{}".format(value.number),
                        description=description))
        return ret