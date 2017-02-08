vatvs_API
!!!!!!!!!


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