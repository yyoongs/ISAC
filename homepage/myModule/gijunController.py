from flask import request , jsonify, render_template
from myModule import counselingdao
import json


class GijunController():
  def __init__(self):
      pass


  def getGijun(self):
      upjong = counselingdao.getGijun()
      return render_template('solution.html', result=upjong)


  def updateTrouble(self):
      selected_class = request.args.get('selected_class', type=str)
      updated_values = counselingdao.getTrouble1(selected_class)

      html_string_selected = ''

      for entry in updated_values:
          html_string_selected += '<option value="{}">{}</option>'.format(entry['type_1'], entry['type_1'])

      return jsonify(html_string_selected=html_string_selected)


  def showGijunTable(self):
      print('hi2')
      selected_upjong = request.args.get('selected_class', type=str)
      selected_trouble1 = request.args.get('selected_entry', type=str)
      result = counselingdao.getStandardBigo(selected_upjong, selected_trouble1)

      return json.dumps(result)


gijunController=GijunController()