vatvs_API
!!!!!!!!!

* (Bo) Query the reference genome used by the variant server?? This is not needed if the variant server accepts multiple reference genomes. 

* (Bo) Set the reference genome (and perhaps format of input) for later queries. For example,
        .. code-block:: python
	        
		@app.route('/vatvs/variants/create_handle')
		def create_connection(refgenome, format='vcf')
		     return None if the server does not support specified refgenome or input format
		     otherwise return a unique ID for connection (something like hg19vcf_89876)
		     
        We should make the "handle" some sort of property of "connection" so that we do not have to
	specify it again.

* (Bo) List annotation databases, their types, and their fields. This would allow the users to specify
	for example gene names using annotation databases defined in the vs.
	.. code-block:: python
		
		@app.route('/vatvs/variants/list_fields')
		def list_fields()
			

* Given varaints information, return variantIDs
	This API will be called from vatdp to get variantIDs for variants in the VCF file. 

	.. code-block:: python

		@app.route('/vatvs/variants/variantsID', methods=['POST'])
		def get_variantsID()


* Given gene name, return variantIDs
	This API will be called from VAT to get variantIDs for a gene.

	.. code-block:: python

		@app.route('/vatvs/variants/gene/<string:geneName>', methods=['GET'])
		def get_variants_in_gene(geneName)

	(Bo): gene is a vague word. We should allow the use of arbitary annotation database,
	something like: refGene.name="ASD". The query will then go to the refGene database
	search for ASD in the field name, get the range of this gene, and find all variants
	within the range. Similarly, users can do refGene_exons.name="ASD". This refGene_exons
	database would store reanges of exons so there are several rows for name ASD (one
	for each exon), and we can then get all variants within the exon regions of the gene.
	Of course there are similar databases for different gene definitions and other "ranges"
	such as cytoband.
	
* Given search criteria, return variantIDs
	This API will be called from VAT to get variantIDs for certain search criteria .

	.. code-block:: python

		@app.route('/vatvs/variants/search', methods=['POST'])
		def search_variants()


* Given gene name, return annotations
	This API will be called from VAT to get annotation for a gene.

	.. code-block:: python

		@app.route('/vatvs/annotation/gene/<string:geneName>', methods=['GET'])
		def get_annotations_by_gene(geneName)

* Given variantID, return annotations
	This API will be called from VAT to get annotation for a variant.

	.. code-block:: python

		@app.route('/vatvs/annotation/variant/<string:variantID>', methods=['GET'])
		def get_annotations_by_variantID(variantID)
