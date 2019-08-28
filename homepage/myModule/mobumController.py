from flask import request
from myModule import counselingdao
from myModule.usadoModel import doc2vec_model
import numpy

class MobumController():
    def __init__(self):
        pass

    def getMobum(self):
        title = request.form.get('inputTitle')
        result1,result2vec, finalResult = doc2vec_model.doc2vec_weight_comp(title)
        return result1,result2vec, finalResult

    def getMobumContent(self, counselID):
        mobumContent = counselingdao.getMobumCounsel(counselID)
        return mobumContent


mobumController = MobumController()