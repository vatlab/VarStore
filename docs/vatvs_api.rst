vatvs_API
!!!!!!!!!



* List annotation databases, their types, and their fields. 
	This API will be called from VAT for users to find out which databases in variant server are available for query. 

	.. code-block:: python
		
		@app.route('/vatvs/variants/list_fields',methods=['GET'])
		def list_fields()
			

* Given varaints information, return variantIDs
	This API will be called from vatdp to get variantIDs for variants in the VCF file. 

	.. code-block:: python

		@app.route('/vatvs/variants/variantsID', methods=['POST'])
		def get_variantIDs()


* Given chromosome and range, return variantIDs
	This API will be called from VAT to get variantIDs for variants in the specified range on a chromosome. 

	.. code-block:: python

		@app.route('/vatvs/variants/<string:chromosome,range>', methods=['GET'])
		def get_variants_by_chromosome_range(chr,range)

* Given fields and range, return variantIDs
	This API will be called from VAT to get variantIDs for variants in the specified range of a field. 

	.. code-block:: python

		@app.route('/vatvs/variants/<string:field,range>', methods=['GET'])
		def get_variants_by_field_range(field,range)


* Given gene name, return variantIDs
	This API will be called from VAT to get variantIDs for a gene. The gene name could be a string specifying which database will be searched, for example 'refGene.name="ASD"'. 

	.. code-block:: python

		@app.route('/vatvs/variants/gene/<string:geneName>', methods=['GET'])
		def get_variants_in_gene(geneName)

	
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

* Given variantIDs, return annotations
	This API will be called from VAT to get annotations for a batch query of variantIDs.

	.. code-block:: python

		@app.route('/vatvs/annotation/variant', methods=['POST'])
		def get_annotations_by_variantIDs([variantIDs])
