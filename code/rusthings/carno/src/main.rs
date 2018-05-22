#[macro_use]
extern crate bson;
extern crate mongodb;
extern crate serde;
#[macro_use]
extern crate serde_derive;

use std::fmt::Debug;

use mongodb::coll::Collection;
use mongodb::db::ThreadedDatabase;
use mongodb::{Client, ThreadedClient};

#[derive(Debug)]
enum RepositoryError {
    MongoError(mongodb::Error),
    DecodeError(bson::DecoderError),
    EncodeError(bson::EncoderError),
}

impl From<mongodb::Error> for RepositoryError {
    fn from(error: mongodb::Error) -> Self {
        RepositoryError::MongoError(error)
    }
}

impl From<bson::EncoderError> for RepositoryError {
    fn from(error: bson::EncoderError) -> Self {
        RepositoryError::EncodeError(error)
    }
}

#[derive(Debug)]
#[allow(dead_code)]
struct BullShit {}

#[derive(Debug, Serialize, Deserialize)]
struct Type1 {
    #[serde(rename = "_id")]
    pub id: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Type2 {
    #[serde(rename = "_id")]
    pub id: String,
}

impl Identifiable for Type1 {
    fn new(id: String) -> Self {
        Self { id: Some(id) }
    }
}

impl Identifiable for Type2 {
    fn new(id: String) -> Self {
        Self { id: id }
    }
}

trait Identifiable {
    fn new(id: String) -> Self;
}

trait Repository<T> {
    fn insert_one(&self, document: T) -> Result<(), RepositoryError>;
    fn find_by_id(&self, id: String) -> Result<Option<T>, RepositoryError>;
}

struct MongoRepository<T> {
    phantom: std::marker::PhantomData<T>,
    collection: Collection,
}

impl<T> MongoRepository<T> {
    pub fn new(coll: Collection) -> Self {
        MongoRepository {
            phantom: std::marker::PhantomData,
            collection: coll,
        }
    }
}

impl<'de, T: Identifiable + serde::Deserialize<'de> + serde::Serialize> Repository<T>
    for MongoRepository<T>
{
    fn insert_one(&self, document: T) -> Result<(), RepositoryError> {
        //let bdoc = bson::to_bson(&document)?;
        //let bson::Bson::Document(ddoc) = bdoc;
        let ddoc = doc!{document};
        match self.collection.insert_one(ddoc, None) {
            Ok(_) => Ok(()),
            Err(err) => Err(RepositoryError::MongoError(err)),
        }
    }

    fn find_by_id(&self, id: String) -> Result<Option<T>, RepositoryError> {
        let doc = doc!{"_id":id};

        let res = self.collection.find_one(Some(doc), None)?;

        match res {
            Some(data) => {
                let bdata = bson::Bson::Document(data);
                let sdata: Result<T, bson::DecoderError> = bson::from_bson(bdata);
                match sdata {
                    Ok(sdoc) => Ok(Some(sdoc)),
                    Err(err) => Err(RepositoryError::DecodeError(err)),
                }
            }
            None => Ok(None),
        }
    }
}

fn find_and_print<Data: Identifiable + Debug, R: Repository<Data>>(t: String, repo: R) {
    let resf = repo.find_by_id("found".to_string());
    let resn = repo.find_by_id("none".to_string());
    let rese = repo.find_by_id("err".to_string());
    println!("{:?} found    : {:?}", t, resf);
    println!("{:?} not found: {:?}", t, resn);
    println!("{:?} error    : {:?}", t, rese);
}

fn main() {
    /* wont build
    let repo_tb: MongoRepository<BullShit> = MongoRepository::new();
    find_and_print(String::from("tb"), repo_tb);
    println!("");
    */

    match Client::with_uri("mongodb://cpsmongo:canopsis@localhost:27017/canopsis") {
        Ok(mgo) => {
            let sid: Result<String, RepositoryError> = Ok(String::from("found"));
            match sid {
                Ok(id) => {
                    let t1 = Type1 { id: Some(id) };
                    let type1_col = mgo.db("canopsis").collection("type1");
                    let type2_col = mgo.db("canopsis").collection("type2");

                    let repo_t1: MongoRepository<Type1> = MongoRepository::new(type1_col);
                    let repo_t2: MongoRepository<Type2> = MongoRepository::new(type2_col);
                    match repo_t1.insert_one(t1) {
                        Ok(_) => {
                            find_and_print(String::from("t1"), repo_t1);
                            /* wont build unless implement Copy trait because repo_t1 moved into find_and_print
    repo_t1.find("bla".to_string());
    */
                            println!("");
                            find_and_print(String::from("t2"), repo_t2);
                        }
                        Err(err) => println!("insert: {:?}", err),
                    }
                }
                Err(err) => println!("object id: {:?}", err),
            }
        }
        _ => panic!("pwet"),
    }
}
