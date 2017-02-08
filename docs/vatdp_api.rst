vatdp_API
!!!!!!!!!


* Given a bag of variants ID, get variants genotypes
	This API will be called from VAT to get genotypes of samples given a bag of variant IDs.

	.. code-block:: python

		@app.route('/vatdp/variants/genotypes', methods=['POST'])
		def get_variants_genotypes()


* Given a sample name, get genotypes of the sample
	This API will be called from VAT to get genotypes of a sample given a sample name.

	.. code-block:: python

		@app.route('/vatdp/samples/genotypes/<string:sampleName>', methods=['GET'])
		def get_sample_genotypes(sampleName)
