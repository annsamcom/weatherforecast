
from flask import Flask,render_template,request,redirect,session,url_for, jsonify
import sqlite3
from datetime import timedelta
import json
app = Flask(__name__)
app.secret_key = "tc,;sv.f;bmgnlmvlrmvlmwdmwsq".encode('utf8')
app.template_folder = "templates"

db = 'ShoppingDB.db'
'''
def connect_db():
    return sqlite3.connect(sqldb)
'''
#lay max id
def get_max_id():
  conn = sqlite3.connect(db)
  #onn = connect_db()
  cursor = conn.cursor()    
  max_id=0
  sqlcommand= "SELECT Max(SupplierID) from Supplier"
  cursor.execute(sqlcommand)
  max_id = cursor.fetchone()[0]
  conn.close()
  return max_id+1

@app.route("/")
def index():
  return "01_CanThuAn_De03"
@app.route("/supplier",methods=["GET"])
def get_Supplier():
  conn = sqlite3.connect(db)
  cursor = conn.cursor()


  cursor.execute("SELECT * FROM Supplier")
  suppliers = cursor.fetchall()

  cursor.close()
  conn.close()
  supplier_list = []
  for supplier in suppliers:
      supplier_dict = {
          'SupplierID': supplier[0],
          'SupplierName': supplier[1],
          'EmailAddress':supplier[2],
          'Password':supplier[3],
          'Tel':supplier[4],
          'TotolEmployee':supplier[5]
      }
      supplier_list.append(supplier_dict)

  return jsonify(supplier_list),200

@app.route("/supplier/<int:id>",methods=["DELETE"])
def delete_Supplier(id):
  supplier_id =id
  if supplier_id:
    try:
      conn = sqlite3.connect(db)
      cursor = conn.cursor()

      cursor.execute("DELETE FROM Supplier WHERE SupplierID = ?", (supplier_id,))
      conn.commit()

 
      if cursor.rowcount == 0:
          return jsonify({'message': 'Khong co supplier nhu the'}), 404

      cursor.close()
      conn.close()

      return jsonify({'message': 'Xoa thanh cong'}), 200

    except sqlite3.Error as e:
      return jsonify({'error': str(e)}), 500
  return jsonify({'message': 'Supplier ID is required'}), 400
@app.route('/Supplier', methods=['POST'])
def add_supplier():
    try:
        data = request.json
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        with connect_db() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Supplier (SupplierName, EmailAddress, Password, Tel, Location) VALUES (?, ?, ?, ?, ?)",
                        (data['supplier_name'], data['email_address'], data['password'], data['tel'], data['location']))

            con.commit()

            cur.execute("SELECT last_insert_rowid()")
            supplier_id = cur.fetchone()[0]

            return jsonify({'supplier_id': supplier_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/supplier",methods=["PUT"])
def update_Supplier():
  try:
    data = request.json 
    supplier_id = data['supplier_id']
    supplier_name = data['supplier_name']

    email_address = data['email_address']
    password = data['password']
    tel = data['tel']
    totol_employee = data['totol_employee']


    if not supplier_id:
        return jsonify({'message': 'SupplierID khong duoc tim thay'}), 400

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    if supplier_name != '':
      cursor.execute("UPDATE Supplier SET supplier_name = ? WHERE SupplierID = ?", (supplier_name, supplier_id))
    if email_address != '':
      cursor.execute("UPDATE Supplier SET EmailAddress = ? WHERE SupplierID = ?", (email_address, supplier_id))
    if password != '':
      cursor.execute("UPDATE Supplier SET Password = ? WHERE SupplierID = ?", (password, supplier_id))
    if tel != '':
      cursor.execute("UPDATE Supplier SET Tel = ? WHERE SupplierID = ?", (tel, supplier_id))
    if totol_employee != '':
      cursor.execute("UPDATE Supplier SET Location = ? WHERE SupplierID = ?", (totol_employee, supplier_id))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Khong tim thay'}), 404

    cursor.close()
    conn.close()

    return jsonify({'message': 'Update thanh cong'}), 200
  except sqlite3.Error as e:
    return jsonify({'error': str(e)}), 500
@app.route("/check",methods=['POST'])
def check():
  try:
    data = request.json
    email_address = data['EmailAddress']
    password = data['Password']
    if not email_address or not password:
        return jsonify({'message': 'Email address va password thieu'}), 400

    # Ket noi csdl
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Check Supplier
    cursor.execute("SELECT * FROM Supplier WHERE Email_address = ? AND Password = ?", (email_address, password))
    supplier = cursor.fetchone()

    # Ngat ket noi csdl
    cursor.close()
    conn.close()
    if supplier:
        return jsonify({'ton tai': True}), 200
    else:
        return jsonify({'ton tai': False}), 200

  except sqlite3.Error as e:
      return jsonify({'error': str(e)}), 500
@app.route("/search",methods=['GET'])
def search_supplier():
  try:
    # Lay thong tin query
    search_query = request.args.get('query') 

    # ket noi csdl
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Tạo truy vấn tìm kiếm
    query = f"""
    SELECT SupplierName,AccountName,EmailAddress FROM Supplier
    WHERE SupplierName LIKE '%{search_query}%' OR
          AccountName LIKE '%{search_query}%' OR
          EmailAddress LIKE '%{search_query}%'
    """
    cursor.execute(query)
    suppliers = cursor.fetchall()

    # Ngat ket noi csdl
    cursor.close()
    conn.close()

    # Chuyển đổi kết quả thành JSON
    suppliers_list = [{'SupplierName': row[0], 'AccountName': row[1], 'EmailAddress': row[2]} for row in suppliers]

    return jsonify(suppliers_list)

  except sqlite3.Error as e:
      return jsonify({'error': str(e)}), 500

@app.route("/addall",methods=["POST"])
def addall():
  suppliers = request.json  # Danh sách các nhà cung cấp
  try:
      # KEt noi cdsl
      conn = sqlite3.connect(db)
      cursor = conn.cursor()

      # Nhap du lieu
      for supplier in suppliers:
          cursor.execute("INSERT INTO Supplier (SupplierID,SupplierName,AccountName,EmailAddress,Password,Tel,TotolEmployee) VALUES (?,?,?,?,?,?)", 
                          (get_max_id(), supplier['SupplierName'],supplier['AccountName'],supplier['EmailAddress'],supplier['Password'],supplier['Tel'],supplier['TotolEmployee']))
      
      conn.commit()

      # Đgat ket noi
      cursor.close()
      conn.close()

      return jsonify({'message': 'Suppliers added successfully'}), 201

  except sqlite3.Error as e:
      return jsonify({'error': str(e)}), 500
if __name__=="__main__":
  app.run(debug=True)