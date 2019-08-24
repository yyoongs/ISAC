from flask import request
from myModule import counselingdao
from myModule.usadoModel import mobum_model


class MobumController():
    def __init__(self):
        pass

    def getMobum(self):
        title = request.form.get('inputTitle')
        print(type(title))
        mobumID,mobumTitle = mobum_model.weight_comp(title)
        return mobumID, mobumTitle

    def getMobumContent(self, counselID):
        mobumContent = counselingdao.getMobumCounsel(counselID)
        return mobumContent


mobumController = MobumController()