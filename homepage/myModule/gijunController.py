from flask import request , jsonify, render_template, redirect
from myModule import counselingdao
import json


class GijunController():
  def __init__(self):
      pass


  def getGijun(self):
      upjong = counselingdao.getGijun()
      return render_template('solution.html', result=upjong)


  def updateTrouble1(self):
      selected_upjong = request.args.get('selected_class', type=str)
      updated_values = counselingdao.getTrouble1(selected_upjong)

      html_string_selected = '<option value="">분쟁유형 1을 선택해주세요</option>'

      for entry in updated_values:
          html_string_selected += '<option value="{}">{}</option>'.format(entry['type_1'], entry['type_1'])

      return jsonify(html_string_selected=html_string_selected)

  def updateTrouble2(self):
      selected_upjong = request.args.get('selected_upjong', type=str)
      selected_trouble1 = request.args.get('selected_trouble1', type=str)
      print(selected_upjong,selected_trouble1)

      if selected_trouble1=='':
          return jsonify(None)


      updated_values = counselingdao.getTrouble2(selected_upjong,selected_trouble1)
      if updated_values[0]['type_2']=='':
          print('이동합니다')
          return jsonify(None)
      #     return redirect('/_show_gijun_table')

      print(updated_values)

      html_string_selected = '<option value="">분쟁유형 2를 선택해주세요</option>'
      # html_string_selected = ''

      for entry in updated_values:
          html_string_selected += '<option value="{}">{}</option>'.format(entry['type_2'], entry['type_2'])
      print(html_string_selected)

      return jsonify(html_string_selected=html_string_selected)

  def updateTrouble3(self):
      selected_upjong = request.args.get('selected_upjong', type=str)
      selected_trouble1 = request.args.get('selected_trouble1', type=str)
      selected_trouble2 = request.args.get('selected_trouble2', type=str)

      print(selected_upjong,selected_trouble1, selected_trouble2)

      if selected_trouble2=='':
          return jsonify(None)

      updated_values = counselingdao.getTrouble3(selected_upjong,selected_trouble1, selected_trouble2)
      if updated_values[0]['type_3']=='':
          print('이동합니다')
          return jsonify(None)

      print(updated_values)
      html_string_selected = '<option value="">분쟁유형 3을 선택해주세요</option>'
      # html_string_selected = ''

      for entry in updated_values:
          html_string_selected += '<option value="{}">{}</option>'.format(entry['type_3'], entry['type_3'])

      return jsonify(html_string_selected=html_string_selected)

  def updateTrouble4(self):
      selected_upjong = request.args.get('selected_upjong', type=str)
      selected_trouble1 = request.args.get('selected_trouble1', type=str)
      selected_trouble2 = request.args.get('selected_trouble2', type=str)
      selected_trouble3 = request.args.get('selected_trouble3', type=str)

      print(selected_upjong,selected_trouble1, selected_trouble2, selected_trouble3)

      if selected_trouble3=='':
          return jsonify(None)


      updated_values = counselingdao.getTrouble4(selected_upjong,selected_trouble1, selected_trouble2, selected_trouble3)
      if updated_values[0]['type_4']=='':
          print('이동합니다')
          return jsonify(None)

      print(updated_values)
      html_string_selected = '<option value="">분쟁유형 4를 선택해주세요</option>'
      # html_string_selected = ''

      for entry in updated_values:
          html_string_selected += '<option value="{}">{}</option>'.format(entry['type_4'], entry['type_4'])

      return jsonify(html_string_selected=html_string_selected)


  def showGijunTable(self):
      print('hi2')
      upjong = request.args.get('upjong', type=str)
      trouble1 = request.args.get('trouble1', type=str)
      trouble2 = request.args.get('trouble2', type=str)
      if trouble2 == None: trouble2 = ''
      trouble3 = request.args.get('trouble3', type=str)
      if trouble3 == None: trouble3 = ''
      trouble4 = request.args.get('trouble4', type=str)
      if trouble4 == None: trouble4 = ''
      print(upjong, trouble1, trouble2, trouble3, trouble4)

      # res = chk2 if chk == () else chk
      # if chk == ():
      #     res = chk2
      # else:
      #     res = chk
      result = counselingdao.getStandardBigo(upjong, trouble1, trouble2, trouble3, trouble4)
      print(result)

      return json.dumps(result)


gijunController=GijunController()