vatdp_API
!!!!!!!!!


* Given a bag of variants ID, get variants genotypes
	This API will be called from VAT to get genotypes of samples given an array of variant IDs.

	.. code-block:: python

		@app.route('/vatdp/variants/genotypes', methods=['POST'])
		def get_genotypes_by_variantIDs()


* Given a sample name, get genotypes of the sample
	This API will be called from VAT to get genotypes of a sample given a sample name.

	.. code-block:: python

		@app.route('/vatdp/samples/genotypes/<string:sampleName>', methods=['GET'])
		def get_genotypes_by_sampleName(sampleName)


* Given a variantID, get metadata for this variant
	This API will be called from VAT to get metadata (e.g. number of samples having this variant) for variant.

	.. code-block:: python

		@app.route('/vatdp/variants/<string:variantID>', methods=['GET'])
		def get_meta_by_variantID(variantID)

* Given a sampleName, get metadata for this sample
	This API will be called from VAT to get metadata (e.g. number of variants in this sample, other stats) for sample.

	.. code-block:: python

		@app.route('/vatdp/samples/<string:sampeName>', methods=['GET'])
		def get_meta_by_sampleName(sampleName)
