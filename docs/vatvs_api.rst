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
		def get_variants_in_gene()
