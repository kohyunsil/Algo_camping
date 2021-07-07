# from flask import *
# from sqlalchemy import and_, or_
# from ..model.place_dao import PlaceDAO as model_place
# from ..util.place_dto import PlaceDTO
#
# place = PlaceDTO
#
# # select tag request
# @place.route('/<keywords>', methods=['GET'])
# class PlaceSearch:
#     def get(self, keywords):
#
#         return jsonify({'abc': keywords})
#
# # url param이 유효하면 이동, 유효하지 않으면 main으로 이동
# @app.route('/search')
# @app.route('/searchlist')
# class PlaceAttr:
#     def get(self):
#         params = request.args.to_dict()
#         split_params = []
#
#         if len(params) == 0 or str(list(params.keys())[0]) != 'keywords':
#             print(str(params.keys()))
#             return redirect('/main', code=302)
#         else:
#             for param in params['keywords'].split(';'):
#                 if param != '':
#                     split_params.append(param)
#
#             # select all test
#             search_all = model_place.query.all()
#             print(search_all)
#
#             return render_template('searchlist.html', keywords=', '.join(split_params), res_num=5)
#
#
