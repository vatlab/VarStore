#!/usr/local/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch import client as client
import json
import logging
import logging.handlers
import sys
import subprocess
import requests 

class AbstractClient(object):
    """
    The abstract superclass of GA4GH Client objects.
    """

    def __init__(self, log_level=0):
        self._log_level = log_level
        logging.basicConfig()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)

    def _deserialize_response(
            self, json_response_string, protocol_response_class):
    	raise NotImplemented()
       




    def _run_search_request(
            self, protocol_request, object_name, protocol_response_class):
       raise NotImplemented()


    def get_dataset(self, dataset_id):
        """
        Returns the Dataset with the specified ID from the server.

        :param str dataset_id: The ID of the Dataset of interest.
        :return: The Dataset of interest.
        :rtype: :class:`ga4gh.protocol.Dataset`
        """
        return self._run_get_request(
            "datasets", protocol.Dataset, dataset_id)

    def get_reference_set(self, reference_set_id):
        """
        Returns the ReferenceSet with the specified ID from the server.

        :param str reference_set_id: The ID of the ReferenceSet of interest.
        :return: The ReferenceSet of interest.
        :rtype: :class:`ga4gh.protocol.ReferenceSet`
        """
        return self._run_get_request(
            "referencesets", protocol.ReferenceSet, reference_set_id)

    def get_reference(self, reference_id):
        """
        Returns the Reference with the specified ID from the server.

        :param str reference_id: The ID of the Reference of interest.
        :return: The Reference of interest.
        :rtype: :class:`ga4gh.protocol.Reference`
        """
        return self._run_get_request(
            "references", protocol.Reference, reference_id)

   

    def get_call_set(self, call_set_id):
        """
        Returns the CallSet with the specified ID from the server.

        :param str call_set_id: The ID of the CallSet of interest.
        :return: The CallSet of interest.
        :rtype: :class:`ga4gh.protocol.CallSet`
        """



    def get_variant(self, variant_id):
        """
        Returns the Variant with the specified ID from the server.

        :param str variant_id: The ID of the Variant of interest.
        :return: The Variant of interest.
        :rtype: :class:`ga4gh.protocol.Variant`
        """


    def get_variant_set(self, variant_set_id):
        """
        Returns the VariantSet with the specified ID from the server.

        :param str variant_set_id: The ID of the VariantSet of interest.
        :return: The VariantSet of interest.
        :rtype: :class:`ga4gh.protocol.VariantSet`
        """


    def search_variants(
            self, variant_set_id, start=None, end=None, reference_name=None,
            call_set_ids=None):
    
        """
        Returns an iterator over the Variants fulfilling the specified
        conditions from the specified VariantSet.

        :param str variant_set_id: The ID of the
            :class:`ga4gh.protocol.VariantSet` of interest.
        :param int start: Required. The beginning of the window (0-based,
            inclusive) for which overlapping variants should be returned.
            Genomic positions are non-negative integers less than reference
            length. Requests spanning the join of circular genomes are
            represented as two requests one on each side of the join
            (position 0).
        :param int end: Required. The end of the window (0-based, exclusive)
            for which overlapping variants should be returned.
        :param str reference_name: The name of the
            :class:`ga4gh.protocol.Reference` we wish to return variants from.
        :param list call_set_ids: Only return variant calls which belong to
            call sets with these IDs. If an empty array, returns variants
            without any call objects. If null, returns all variant calls.

        :return: An iterator over the :class:`ga4gh.protocol.Variant` objects
            defined by the query parameters.
        :rtype: iter
        """

 

    def search_datasets(self):
        """
        Returns an iterator over the Datasets on the server.

        :return: An iterator over the :class:`ga4gh.protocol.Dataset`
            objects on the server.
        """


    def search_variant_sets(self, dataset_id):
        """
        Returns an iterator over the VariantSets fulfilling the specified
        conditions from the specified Dataset.

        :param str dataset_id: The ID of the :class:`ga4gh.protocol.Dataset`
            of interest.
        :return: An iterator over the :class:`ga4gh.protocol.VariantSet`
            objects defined by the query parameters.
        """


   
    def search_call_sets(self, variant_set_id, sample_id=None):
        """
        Returns an iterator over the CallSets fulfilling the specified
        conditions from the specified VariantSet.

        :param str variant_set_id: Find callsets belonging to the
            provided variant set.
        :param str name: Only CallSets matching the specified name will
            be returned.
        :param str bio_sample_id: Only CallSets matching this id will
            be returned.
        :return: An iterator over the :class:`ga4gh.protocol.CallSet`
            objects defined by the query parameters.
        """
       

    def get_variant():


    def get_variants():


    def get_cell():



class ESClient(AbstractClient):

    def __init__(self):
        super(ESClient, self).__init__(logLevel)
        syscall = subprocess.run(["docker-machine","ip","default"],stdout=subprocess.PIPE)
		self.dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
		self.elasticsearch_port = "9252"
		self.index    = 'vatdp'
		self.doctype  = 'vatdp'


	def runQuery(self,query):	
		url = "http://"+self.dockermachine_hostname+":"+self.elasticsearch_port+"//"+self.index+"/"+self.doctype+"/_search"
		response = requests.post(url,data=json.dumps(query))
		return json.loads(response.text)


	def get_variants(self,ids):
		query = {}
		query["query"] = {}
		query["query"]["bool"] = {}
		query["query"]["bool"]["must"]=[]
		query["query"]["bool"]["must"].append({"terms" : { "variantID" : [ids] }})
		query["size"]   = len(ids)
		result=self.runQuery(query)
		return result

	def get_Sample_Genotype(self,sample):
		query={}
		query["query"]={}
		query["query"]["nested"]={}
		query["query"]["nested"]["path"]="Genotype"
		query["query"]["nested"]["query"]={}
		query["query"]["nested"]["query"]["bool"]={}
		query["query"]["nested"]["query"]["bool"]["must"]=[]
		query["query"]["nested"]["query"]["bool"]["must"].append({"term":{"Genotype.sampleName":sample}})
		result=self.runQuery(query)
		return result
        







