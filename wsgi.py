import pymysql
from application import application
from db_config import mysql
from flask import jsonify
from flask import flash, request

def find_rank(obj, detections):
    detection_arr = detections.split(';;')
    matching = [i-1 for i, elem in enumerate(detection_arr) if elem == obj]
    if len(matching) == 0:
        print('warning: find_rank returning -1')
        return -1
    else:
        return matching[0]

@application.route('/allfiles')
def allfiles():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        query_str = request.args.get('query')
        sqlQuery = "select * from fileobj"
        if query_str:
            whereClause = " where " + query_str
            sqlQuery += whereClause
        cur.execute(sqlQuery + ";")
        rows = cur.fetchall()

        mapped = []
        for row in rows:
            if 'filename' in row and 'path' in row:
                filename = row['filename']
                path = row['path']
                row['filename'] = '<a target="_blank" href="http://medsieve-mgr.almaden.ibm.com:8080' + path.replace('/gpfs/fs0/data', '') + filename + '">' + filename + '</a>'
            mapped.append({k.replace("_", ""): v for k, v in row.items()})

        # custom code for resorting rows for ZSL case
        if query_str:
            comps = query_str.split(' ')
            if len(comps) == 3:
                if comps[0] == 'zsl1' and comps[1] == 'like':
                    valComps = comps[2].split(';')
                    if len(valComps) == 3:
                        tag = comps[0]
                        obj = valComps[1]
                        # compute rank of 'obj' in 'tag', create new column for sorting
                        for row in mapped:
                            row['zslrank'] = find_rank(obj, row[tag])
                        mapped = sorted(mapped, key=lambda k: k['zslrank'])
        # end custom resorting code

        resp = jsonify(mapped)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@application.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
