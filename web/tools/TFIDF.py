from math import log10
import numpy as np

class TFIDFTool():
    def __calculate_ddf(self, documents_tf: dict) -> dict:
        result = {}
        df_list = {}
        for term, tf in documents_tf.items():
            df = 0
            for f in tf:
                df += 1 if f > 0 else 0
                df_list[term] = df
            result[term] = len(tf) / df
        
        self.df = result
        return {
            "result" : result,
            "df_list" : df_list
        }
    
    def _calculate_idf(self, df_list: dict) -> dict:
        result = {}
        for term, df in df_list.items():
            result[term] = log10(df) + 1
        return result

    def process(self, documents_tf: dict) -> dict:
        result = {}
        ddf_list = self.__calculate_ddf(documents_tf=documents_tf)
        idf_list = self._calculate_idf(df_list=ddf_list["result"])

        for term, tfs in documents_tf.items():
            result[term] = [tf*idf_list[term] for tf in tfs]
        
        self.result = result
        return {
            "ddf_list" : ddf_list["result"],
            "df_list": ddf_list["df_list"],
            "idf_list": idf_list,
            "tf_idf_list" : result
        }

    def rank(self, query):
        result_list = {}
        for key in query["result"]:
            if key in self.result:
                rank_list = self.result[key]
                for index, element in enumerate(rank_list):
                    if len(result_list) <= index :
                        result_list[index] = element
                    else:
                        result_list[index] += element
        keys = list(result_list.keys())
        values = list(result_list.values())
        sorted_value_index = np.argsort(values)[::-1]
        result_list = {keys[i]: values[i] for i in sorted_value_index}

        return result_list