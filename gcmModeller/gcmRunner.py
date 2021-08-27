"""Please follow the format as shown in the two sample input datasets.  The formatting is quite strict to that standard.  More work could be done to accept a variety of formatting for datasets.  

Please contact us at <jlhoeflinger@ucdavis.edu> for help troubleshooting problems.

To run the code with the example datasets run the following:"""

import GrowthCurveModeler as gcm

def main():
  gcm.GrowthCurveModeler('RA_example_gcm_data.xlsx', threshold=0.01)


if __name__ == "__main__":
    main()


