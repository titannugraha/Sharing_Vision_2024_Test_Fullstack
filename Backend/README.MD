1. Perintahnya menggunakan cara manual, saya memakai syntax sql 
CREATE TABLE posts (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(200),
    Content TEXT,
    Category VARCHAR(100),
    Created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Status VARCHAR(100) CHECK (Status IN ('Publish', 'Draft', 'Thrash'))
);


2. Saya membuat nya secara manual di phpmyadmin, karena di flask-migrate dengan mysql tidak bisa membuat database secara otomatis.
lalu saya membuat file migrasi untuk membuat tabel posts dan memigrate nya ke database dengan flask db migrate dan flask db upgrade.

3. Membuat endpoint   
a./article - Method POST. Saya menggunakan transaction database agar menghindari jika ada proses yang gagal, maka data tidak jadi dimasukan ke database. dan juga saya menggunakan validasi agar tidak ada data yang kosong.
b./article/offset/limit - GET. Saya menggunakan ORM dari flask-sqlalchemy untuk mempermudah mengambil data dengan limit dan offset yang diambil dari parameter offset dan limit. Lalu saya juga membuat validai jika tidak ada data nya, serta memakai try catch, untuk menangkap error yang terjadi jika ada kesalahan.
c./article/id - GET. Saya menggunakan ORM dari flask-sqlalchemy untuk mempermudah mengambil data berdasarkan id. Lalu saya juga membuat validai jika tidak ada data nya, serta memakai try catch, untuk menangkap error yang terjadi jika ada kesalahan.
d./article/id - PUT. Saya mencari data berdasarkan id, lalu update data berdasarkan id. Lalu saya juga membuat validai jika tidak ada data nya, serta memakai try catch, untuk menangkap error yang terjadi jika ada kesalahan.
e./article/id - DELETE. Saya mencari data berdasarkan id, lalu delete data berdasarkan id.

4. Saya membuat fungsi validate_article dengan parameter title, content, category, status yang masih dibalut dengan json.Lalu memanggil fungsi tersebut didalam, endpoint yang menggunakan request atau yang menggunakan method POST dan PUT yaitu di endpoint untuk membuat dan mengubah, yang mengembalikan pesan dan kode ke endpoint, dan jika tidak 200 kode nya maka akan mengembalikan pesan kesalahan berbentuk jsono

5. [text](<./Test Backend - Sharing Vision 2021.postman_collection.json>)


