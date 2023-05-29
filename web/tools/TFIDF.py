from math import log10

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
        
        return {
            "ddf_list" : ddf_list["result"],
            "df_list": ddf_list["df_list"],
            "idf_list": idf_list,
            "tf_idf_list" : result
        }