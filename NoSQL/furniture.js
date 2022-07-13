use furniture

/*поставщики*/
suppl1={
    //"Id" : 1,
    "Name":"Pinskdrev",
    "Address":"Malinovka",
    "Manager":"Polina",
    "Start_date": Date("2010-07-20T18:00:00Z"),
    "End_date": Date("2022-07-20T18:00:00Z")}

suppl2={
    //"Id":2,
    "Name":"IKEA",
    "Address":"Poland",
    "Manager":"Zahar",
    "Start_date": Date("2013-01-20T18:00:00Z"),
    "End_date": Date("2023-01-20T18:00:00Z")}
    
suppl3={
    //"Id":3,
    "Name":"AMI Mebel",
    "Address":"Minsk",
    "Manager":"Stephan",
    "Start_date": Date("2019-04-20T18:00:00Z"),
    "End_date": Date("2024-04-20T18:00:00Z")}
    
suppl4={
   // "Id":4,
    "Name":"MillWood",
    "Address":"Minsk",
    "Manager":"Anna",
    "Start_date": Date("2016-04-20T18:00:00Z"),
    "End_date": Date("2024-04-20T18:00:00Z")} 
    
/*Оптимизация заключается в том, что мы делаем один запрос в базу вместо того, чтобы добавлять каждый документ отдельно*/

db.suppliers.insertMany([suppl1,suppl2, suppl3, suppl4])

suppl1 = db.suppliers.findOne({"Name":"Pinskdrev"})

/*материалы*/
m1={
    "Name":"Birch",
    "Cost":50,
    "Desc":
        {"quality":"average",
        "color":"light"},
    Supplier: new DBRef("suppliers", suppl1._id)
}

suppl2 = db.suppliers.findOne({"Name":"IKEA"})


m2={
    "Name":"Aspen",
    "Cost":100,
    "Desc": 
        {"quality":"good",
        "color":"light"},
    Supplier: new DBRef("suppliers", suppl2._id)
}


m3 ={
    "Name":"Metal",
    "Cost":450,
    "Desc": 
        {"quality":"good",
        "color":"silver"},
    Supplier: new DBRef("suppliers", suppl2._id)
}

m4={
    "Name":"Bamboo",
    "Cost":550,
    "Desc": 
        {"quality":"premium",
        "color":"light brown"},
    Supplier: new DBRef("suppliers",  suppl1._id)
}

m5={
    "Name":"Glass",
    "Cost":40,
    "Desc": 
        {"quality":"average",
        "color":"opacity"},
    Supplier: new DBRef("suppliers", suppl1._id)
}

m6={
    "Name":"Oak",
    "Cost":140,
    "Desc": 
        {"quality":"good",
        "color":"brown"},
    Supplier: new DBRef("suppliers", suppl1._id)
}

db.materials.insertMany([m1,m2,m3,m4,m5,m6])

/*товары*/
item1 = {
    "Name":"Bamboo Dresser",
    "Type":["bedroom","living room"],
    "Desc":"Elegant and lovely design, made with eco-friendly materials",
    "Material": m4,
    "Cost":850,
    "Amount": 12 /*сколько на складе*/
}

item2=
{
    "Name":"Wardrobe",
    "Type":"bedroom",
    "Desc":"Big wardrobe made from oak to keep your clothes",
    "Material": [m5, m6],
    "Cost":1000,
    "Amount":8
}

item3=
{
    "Name":"Cupboard",
    "Type":["kitchen","dining room"],
    "Desc":"Very modern and stylish",
    "Material": [m3,m5],
    "Cost":550,
    "Amount":25
}

item4=
{
    "Name":"Bookcase",
    "Type":"living room",
    "Desc":"For your personal library",
    "Material": [m2, m5],
    "Cost":600,
    "Amount":10
}

item5=
{
    "Name":"Closet",
    "Type":"bedroom",
    "Desc":"Build-in closet too keep your outfits",
    "Material": [m2, m3],
    "Cost":1200,
    "Amount":14
}

db.shop.items.insertMany([item1, item2, item3, item4, item5])

/*заказы*/
order1=
{
    "Start_date":Date("2022-05-08T14:00:00Z"),
    "Delivery_date": Date("2022-05-18T16:00:00Z"),
    "Name":"Veranika Stepanova",
    "Personal_info": 
        {"email":"veronstep@gmail.com",
         "adress":"Minsk, Korolya 2",
         "membership":"vip"},
    "Items":[item1, item3]
}

order2=
{
    "Start_date":Date("2022-05-10T18:00:00Z"),
    "Delivery_date": Date("2022-06-17T13:00:00Z"),
    "Name":"Egor Egorovich",
    "Personal_info": 
        {"email":"egorka123@gmail.com",
         "adress":"Minsk, Sverdova 15",
        "membership":"unknown"},
    "Items":item2
}

order3=
{
    "Start_date":Date("2022-05-09T14:00:00Z"),
    "Delivery_date": Date("2022-05-23T16:00:00Z"),
    "Name":"Alla Pugacheva",
    "Personal_info": 
        {"email":"allapug@gmail.com",
         "adress":"Moscow, Pushkinskaya 8",
        "membership":"usual"},
    "Items":item1
}

order4=
{
    "Start_date":Date("2022-05-10T14:00:00Z"),
    "Delivery_date": Date("2022-05-26T18:00:00Z"),
    "Name":"Darya Domracheva",
    "Personal_info": 
        {"email":"dariasport@gmail.com",
         "adress":"Gomel, Minskaya 8",
        "membership":"vip"},
    "Items": [item1, item3, item4]
}

order5=
{
    "Start_date":Date("2022-05-11T17:00:00Z"),
    "Delivery_date": Date("2022-05-26T16:00:00Z"),
    "Name":"Peter Petrov",
    "Personal_info": 
        {"email":"peterpeter12@gmail.com",
         "adress":"Moscow, Lenina 2",
        "membership":"unknown"},
    "Items": [item1, item3, item4]
}

order6=
{
    "Start_date":Date("2022-05-01T17:00:00Z"),
    "Delivery_date": Date("2022-05-11T16:00:00Z"),
    "Name":"Ivan Ivanov",
    "Personal_info": 
        {"email":"ivanov@gmail.com",
         "adress":"Minsk, Gamarnika 10",
        "membership":"unknown"},
    "Items": item5
}

db.shop.orders.insertMany([order1,order2, order3, order4, order5, order6])

