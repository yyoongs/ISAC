from flask import request, jsonify, render_template
from datetime import datetime
from myModule import counselingdao
from settings import APP_STATIC
from keras import backend as K
from keras.models import load_model
import pandas as pd
import json
import os
from myModule.getSolutionController import getSolution
from keras import optimizers
import pickle
import numpy as np
from keras.preprocessing.sequence import pad_sequences
maxlen = 50
tokenizer = pickle.load(open('./static/tokenizer.pkl', 'rb'))


class CounselController():
    def __init__(self):
        pass


    def getBigcate(self):
        bigCate = counselingdao.getBigCate()
        return render_template('index.html', big_cate=bigCate)


    def updateMidcate(self):
        selected_class = request.args.get('selected_big', type=str)
        updated_values = counselingdao.getMidCate(selected_class)

        html_string_selected='<option value="">전체</option>';
        for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry['mname'], entry['mname'])

        return jsonify(html_string_selected=html_string_selected)


    def updateSmallcate(self, bigCate, midCate):
        updated_values = counselingdao.getSmallCate(bigCate, midCate)

        html_string_selected = '<option value="">전체</option>';
        for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry['sname'], entry['sname'])

        return jsonify(html_string_selected=html_string_selected)


    # 상담글 작성
    def writeCounsel(self):
        title = request.form.get('inputTitle')
        big = request.form.get('SelectBigCate')
        mid = request.form.get('SelectMidCate')
        small = request.form.get('SelectSmallCate')
        question_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        question = request.form.get('inputContent')

        # 답변을 여기다가 넣기

        counsel = {'title': title, 'big_cate': big, 'mid_cate': mid, 'small_cate': small,
                   'question_date': question_date,
                   'question': question}
        tags, gijun, cname = getSolution(counsel)
        print(tags)
        if gijun == -1:
            gijun = '고객님이 질문하신 내용에 대한 적당한 해결기준을 찾지 못하였습니다.'
        # counsel['tags'] = tags
        # counsel['answer'] = gijun
        counselingdao.setCounseling(counsel)
        result = counselingdao.getCounseling(question_date)
        print('gijun은 ', gijun)

        # counselingdao.setTagsresult[0]['id']

        # 들어온 상담에 대해서 결과값 출력
        # gijun = getSolution(counsel)

        return result, tags, gijun, cname


    # 모델을 통한 예측
    def predictModel(self, tags, cname):
        optimizer = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
        addPaperModel = load_model(os.path.join(APP_STATIC, 'predictModel/_ultimate_add_paper.h5'))
        addPaperModel.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        goojaeModel = load_model(os.path.join(APP_STATIC, 'predictModel/_ultimate_goojae.h5'))
        goojaeModel.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        jojungModel = load_model(os.path.join(APP_STATIC, 'predictModel/_ultimate_jojung.h5'))
        jojungModel.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        negoableModel = load_model(os.path.join(APP_STATIC, 'predictModel/_ultimate_nego_able.h5'))
        negoableModel.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        temp = tokenizer.texts_to_sequences(tags)
        temp = pad_sequences(temp, padding='post', maxlen=maxlen)
        inputList = list()


        for i in range(len(temp)):
            if len(inputList) != 50:
                inputList.append(temp[i][0])
            else:
                break
        for i in range(50):
            inputList.append(0)
            if len(inputList) == 50:
                break
        inputList = np.array(inputList, dtype='int32').reshape(1, -1)

        con1 = int(str(addPaperModel.predict(inputList)[0][0])[2:4])
        con2 = int(str(negoableModel.predict(inputList)[0][0])[2:4])
        con3 = int(str(jojungModel.predict(inputList)[0][0])[2:4])
        con4 = int(str(goojaeModel.predict(inputList)[0][0])[2:4])

        text = " 안녕하십니까, 아이작입니다. 상담해주신 내용 잘 읽었습니다. 위의 단어들을 확인해보시면 제가 어떤 부분을 바탕으로 이해를 했는지 확인을 하실 수 있습니다 :)" \
               " 결과를 알려드리기 이전, 아이작은 법적인 효력이 없기 때문에 이점 참고 부탁드립니다. 아래의 네 가지 숫자들은 각각 이용자님께서 어떤 선택을 해야 하는지" \
               "알려드리는 지표입니다. 파란색으로 표시된 부분을 참고하시면 됩니다. 그럼, 제가 분석한 결과는 다음과 같습니다."

        if con2>50 and con3>50:
            if (con4>50):
                if (con2>con4) or (con3>con4):
                    if (con1>50) and (cname):
                        text += "|@ 이용자님의 상황에 대해서는 상대적으로 쉽게 구제 가능합니다. 따라서 위에 제공된 해결 기준을 바탕으로 직접 " \
                               "사업자와 합의를 도출하셔도 괜찮을 것이라고 판단됩니다.$ 만약 합의 도출에 실패하시거나 곧바로 구제 신청을 하시려면 다음을 참고하시길 바랍니다." \
                               "| <피해구제 접수방법> 우리원 홈페이지(www.kca.go.kr)  피해구제-‘피해구제신청’ 에서 피해구제신청서를 다운받아 작성하시고, 피해구제신청서와 함께 관련 입증자료을 첨부하여 팩스, 우편 등을 이용하여 보내주시면 됩니다."\
                               "-보내실 곳 : 한국소비자원 피해구제1국 1372 지원팀  (주소) 서울 서초구 양재대로 246(염곡동), (우편번호 137-700) (팩스) 02) 3460-3180" \
                               "※ 서류가 도착되면 근무시간 기준 24시간내 서류가 도착되었음을 피해구제 신청서에 기록된 휴대폰 문자로 알려 드립니다."
                if con1 > 50:
                    text += " |@ 또한, 보다 정확한 상황 파악을 위해 추가서류 제출도 필요하다고 판단됩니다.$ " \
                            "추가 서류는 영수증 사본, 계약서 사본, 증명서 등과 같이 법적효력을 확인할 수 있는 서류들을 의미하며, " \
                            "이용자님의 상황을 보다 정확히 판단하는 동시에 상황을 해결하는데 적극적으로 활용되기 때문에 제출하신다면 해결 가능성을 보다 높일 수 있습니다." \
                            "구제 서류 제출시 관련 서류도 같이 제출하시면 보다 빨리 문제를 해결하실 수 있습니다."
            else:
                if cname:
                    text += "|@이용자님과 같은 상황에서는 보통 위에 제공된 기준들을 바탕으로 사업자와 합의를 도출해볼 것을 권고해드리고 있습니다.$" \
                           "이와 같은 방법으로도 해결이 될 가능성이 높기 때문에 먼저 시도해보시고 이후 합의 도출이 되지 않는다면 구제 신청서를 제출해주시길 바랍니다."

                else:
                    text += "|@이용자님과 같은 상황은 상대적으로 해결하기 쉽습니다.$ ISAC 홈페이지에서 제공되는 민원 해결 기준과 관련 민원을 찾아보고, " \
                           "이를 활용해서 사업자와 직접 합의 도출을 시도해보시길 바랍니다."
        elif con2>50 and con3<50:
            if con4>50:
                if con2>con4:
                    if cname:
                        text += "|@이용자님과 유사한 많은 사례들이 쉽게 해결 가능했습니다. 구제 신청도 가능하시며, 이용자님께서 위에 언급된 기준을 참고하여" \
                                "직접 사업자와 합의를 도출하셔도 된다고 판단됩니다.$ 만약 혼자 해결하기에 꺼려지신다면 구제 신청서를 제출하시길 바랍니다." \
                               "| <피해구제 접수방법> 우리원 홈페이지(www.kca.go.kr)  피해구제-‘피해구제신청’ 에서 피해구제신청서를 다운받아 작성하시고, 피해구제신청서와 함께 관련 입증자료을 첨부하여 팩스, 우편 등을 이용하여 보내주시면 됩니다."\
                               "-보내실 곳 : 한국소비자원 피해구제1국 1372 지원팀  (주소) 서울 서초구 양재대로 246(염곡동), (우편번호 137-700) (팩스) 02) 3460-3180" \
                               "※ 서류가 도착되면 근무시간 기준 24시간내 서류가 도착되었음을 피해구제 신청서에 기록된 휴대폰 문자로 알려 드립니다."
                    else:
                        text += "|@이용자님과 유사한 많은 사례들이 쉽게 해결 가능했습니다. 구제 신청도 가능하시며, 이용자님께서 " \
                                "직접 사업자와 합의를 도출하셔도 된다고 판단됩니다.$ 해결 기준을 참고하시고 싶으시다면 오른쪽에 제시된 관련 민원이나 " \
                                "아이작 홈페이지에서 제공되는 해결 기준을 이용하시길 바랍니다." \
                                "만약 혼자 해결하기에 꺼려지신다면 구제 신청서를 제출하셔서 구제를 받으시길 바랍니다." \
                               " <피해구제 접수방법> 우리원 홈페이지(www.kca.go.kr)  피해구제-‘피해구제신청’ 에서 피해구제신청서를 다운받아 작성하시고, 피해구제신청서와 함께 관련 입증자료을 첨부하여 팩스, 우편 등을 이용하여 보내주시면 됩니다."\
                               "-보내실 곳 : 한국소비자원 피해구제1국 1372 지원팀  (주소) 서울 서초구 양재대로 246(염곡동), (우편번호 137-700) (팩스) 02) 3460-3180" \
                               "※ 서류가 도착되면 근무시간 기준 24시간내 서류가 도착되었음을 피해구제 신청서에 기록된 휴대폰 문자로 알려 드립니다."
                else:
                    text += "|@이런 경우 이용자님께서 직접 사업자와 협의를 도출하실 수도 있지만, 구제 신청서 제출이라는, 보다 더 확실한 방법을 추천 드립니다.$" \
                            "| <피해구제 접수방법> 우리원 홈페이지(www.kca.go.kr)  피해구제-‘피해구제신청’ 에서 피해구제신청서를 다운받아 작성하시고, 피해구제신청서와 함께 관련 입증자료을 첨부하여 팩스, 우편 등을 이용하여 보내주시면 됩니다."\
                               "-보내실 곳 : 한국소비자원 피해구제1국 1372 지원팀  (주소) 서울 서초구 양재대로 246(염곡동), (우편번호 137-700) (팩스) 02) 3460-3180" \
                               "※ 서류가 도착되면 근무시간 기준 24시간내 서류가 도착되었음을 피해구제 신청서에 기록된 휴대폰 문자로 알려 드립니다."
                if con1 > 50:
                    text += " |@또한, 보다 정확한 상황 파악을 위해 추가서류 제출도 필요하다고 판단됩니다.$ " \
                                "추가 서류는 영수증 사본, 계약서 사본, 증명서 등과 같이 법적효력을 확인할 수 있는 서류들을 의미하며, " \
                                "이용자님의 상황을 보다 정확히 판단하는 동시에 상황을 해결하는데 적극적으로 활용되기 때문에 제출하신다면 해결 가능성을 보다 높일 수 있습니다." \
                                "구제 서류 제출시 관련 서류도 같이 제출하시면 보다 빨리 문제를 해결하실 수 있습니다."
            else:
                if cname:
                    text += "|@이용자님의 같은 상황에서는 구제 신청서 작성까지 필요가 없을 것으로 판단됩니다. 상단에 제공된 해결 기준을 바탕으로 사업자와 합의점을 도출할 수 있기 때문에" \
                            "시도해보시길 바랍니다.$"
                else:
                    text = "|@이용자님의 같은 상황에서는 구제 신청서 작성까지 필요가 없을 것으로 판단됩니다.$ 해결 기준을 바탕으로 사업자와 합의점을 도출할 수 있기 때문에" \
                            "시도해보시길 바랍니다. 해결 기준은 오른쪽의 모범 상담을 참고하시거나, 아이작 홈페이지 상단에서 확인하실 수 있습니다."
        elif con2<50 and con3>50:
            if con4>50:
                text+="|@이용자님의 상황과 같은 경우에는 곧바로 구제 신청을 하시는 것을 권고해드리고 있습니다. 이용자님께서 직접 해결을 시도하시거나" \
                      "소비자 상담센터에서 전화로 합의를 권고하는 것으로는 해결이 어려워 보입니다. 곧바로 구제 신청을 하시길 바랍니다.$" \
                      "| <피해구제 접수방법> 우리원 홈페이지(www.kca.go.kr)  피해구제-‘피해구제신청’ 에서 피해구제신청서를 다운받아 작성하시고, 피해구제신청서와 함께 관련 입증자료을 첨부하여 팩스, 우편 등을 이용하여 보내주시면 됩니다." \
                      "-보내실 곳 : 한국소비자원 피해구제1국 1372 지원팀  (주소) 서울 서초구 양재대로 246(염곡동), (우편번호 137-700) (팩스) 02) 3460-3180" \
                      "※ 서류가 도착되면 근무시간 기준 24시간내 서류가 도착되었음을 피해구제 신청서에 기록된 휴대폰 문자로 알려 드립니다."
            else:
                text+="|@다른 사건들에 비하여 상대적으로 쉽게 해결되는 상황이지만 이용자님께서 직접 협상을 시도할 상황은 아니라고 판단됩니다.$" \
                      " 따라서 구제 신청을 통해 보다 빠르고 안전하게 상황을 해결하시길 바랍니다." \
                      "| <피해구제 접수방법> 우리원 홈페이지(www.kca.go.kr)  피해구제-‘피해구제신청’ 에서 피해구제신청서를 다운받아 작성하시고, 피해구제신청서와 함께 관련 입증자료을 첨부하여 팩스, 우편 등을 이용하여 보내주시면 됩니다." \
                      "-보내실 곳 : 한국소비자원 피해구제1국 1372 지원팀  (주소) 서울 서초구 양재대로 246(염곡동), (우편번호 137-700) (팩스) 02) 3460-3180" \
                      "※ 서류가 도착되면 근무시간 기준 24시간내 서류가 도착되었음을 피해구제 신청서에 기록된 휴대폰 문자로 알려 드립니다."
            if con1 > 50:
                text += " |@또한, 보다 정확한 상황 파악을 위해 추가서류 제출도 필요하다고 판단됩니다.$ " \
                            "추가 서류는 영수증 사본, 계약서 사본, 증명서 등과 같이 법적효력을 확인할 수 있는 서류들을 의미하며, " \
                            "이용자님의 상황을 보다 정확히 판단하는 동시에 상황을 해결하는데 적극적으로 활용되기 때문에 제출하신다면 해결 가능성을 보다 높일 수 있습니다." \
                            "구제 서류 제출시 관련 서류도 같이 제출하시면 보다 빨리 문제를 해결하실 수 있습니다."
        else:
            if con4>50:
                text += "|@이용자님의 상황과 같은 경우에는 곧바로 구제 신청을 하시는 것을 권고해드리고 있습니다. 이용자님께서 직접 해결을 시도하시거나" \
                      "소비자 상담센터에서 전화로 합의를 권고하는 것으로는 해결이 어려워 보입니다. 곧바로 구제 신청을 하시길 바랍니다.$" \
                      "| <피해구제 접수방법> 우리원 홈페이지(www.kca.go.kr)  피해구제-‘피해구제신청’ 에서 피해구제신청서를 다운받아 작성하시고, 피해구제신청서와 함께 관련 입증자료을 첨부하여 팩스, 우편 등을 이용하여 보내주시면 됩니다." \
                      "-보내실 곳 : 한국소비자원 피해구제1국 1372 지원팀  (주소) 서울 서초구 양재대로 246(염곡동), (우편번호 137-700) (팩스) 02) 3460-3180" \
                      "※ 서류가 도착되면 근무시간 기준 24시간내 서류가 도착되었음을 피해구제 신청서에 기록된 휴대폰 문자로 알려 드립니다."
                if con1 > 50:
                    text += " |@또한, 보다 정확한 상황 파악을 위해 추가서류 제출도 필요하다고 판단됩니다.$ " \
                            "추가 서류는 영수증 사본, 계약서 사본, 증명서 등과 같이 법적효력을 확인할 수 있는 서류들을 의미하며, " \
                            "이용자님의 상황을 보다 정확히 판단하는 동시에 상황을 해결하는데 적극적으로 활용되기 때문에 제출하신다면 해결 가능성을 보다 높일 수 있습니다." \
                            "구제 서류 제출시 관련 서류도 같이 제출하시면 보다 빨리 문제를 해결하실 수 있습니다."
            else:
                text += "|@이런 경우에는 구제 불가능합니다. 죄송합니다.$"


        K.clear_session()
        model_res = [con1, con2, con3, con4]
        print(model_res)
        return model_res, text

counselController = CounselController()
