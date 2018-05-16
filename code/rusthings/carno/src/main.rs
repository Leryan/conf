extern crate bson;
extern crate mongodb;
extern crate serde;
#[macro_use]
extern crate serde_derive;

use std::fmt::Debug;

use bson::Document;
use mongodb::coll::Collection;
use mongodb::db::ThreadedDatabase;
use mongodb::{Client, ThreadedClient};

#[derive(Debug)]
enum RepositoryError {
    IOError(String),
    MongoError(mongodb::Error),
    DocumentError(bson::DecoderError),
}

#[derive(Debug)]
#[allow(dead_code)]
struct BullShit {}

#[derive(Debug, Serialize, Deserialize)]
struct Type1 {
    #[serde(rename = "_id")]
    pub id: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct Type2 {
    #[serde(rename = "_id")]
    pub id: String,
}

impl Identifiable for Type1 {
    fn new(id: String) -> Self {
        return Self { id: id };
    }
}

impl Identifiable for Type2 {
    fn new(id: String) -> Self {
        return Self { id: id };
    }
}

trait Identifiable {
    fn new(id: String) -> Self;
}

trait Repository<T: Identifiable> {
    fn find_by_id(&self, id: String) -> Result<Option<T>, RepositoryError>;
}

struct GenericRepository<T> {
    phantom: std::marker::PhantomData<T>,
    collection: Collection,
}

impl<T> GenericRepository<T> {
    pub fn new(coll: Collection) -> Self {
        return GenericRepository {
            phantom: std::marker::PhantomData,
            collection: coll,
        };
    }
}

impl<'de, T: Identifiable + serde::Deserialize<'de>> Repository<T> for GenericRepository<T> {
    fn find_by_id(&self, id: String) -> Result<Option<T>, RepositoryError> {
        let mut doc = Document::new();
        doc.insert("_id", id);
        let res = self.collection.find_one(Some(doc), None);
        match res {
            Ok(data) => match data {
                Some(cdata) => {
                    let tt: Result<T, bson::DecoderError> =
                        bson::from_bson(bson::Bson::Document(cdata));
                    match tt {
                        Ok(t) => return Ok(Some(t)),
                        Err(err) => return Err(RepositoryError::DocumentError(err)),
                    };
                }
                None => Ok(None),
            },
            Err(err) => Err(RepositoryError::MongoError(err)),
        }
    }
}

fn find_and_print<Data: Identifiable + Debug, R: Repository<Data>>(t: String, repo: R) {
    let resf = repo.find_by_id("found".to_string());
    let resn = repo.find_by_id("none".to_string());
    let rese = repo.find_by_id("err".to_string());
    println!("{:?} found: {:?}", t, resf);
    println!("{:?} not found: {:?}", t, resn);
    println!("{:?} error: {:?}", t, rese);
}

fn main() {
    /* wont build
    let repo_tb: GenericRepository<BullShit> = GenericRepository::new();
    find_and_print(String::from("tb"), repo_tb);
    println!("");
    */

    let mgo = Client::with_uri("mongodb://cpsmongo:canopsis@localhost:27017/canopsis").unwrap();
    let type1_col = mgo.db("canopsis").collection("type1");
    let type2_col = mgo.db("canopsis").collection("type2");

    let repo_t1: GenericRepository<Type1> = GenericRepository::new(type1_col);
    let repo_t2: GenericRepository<Type2> = GenericRepository::new(type2_col);
    find_and_print(String::from("t1"), repo_t1);
    /* wont build unless implement Copy trait because repo_t1 moved into find_and_print
    repo_t1.find("bla".to_string());
    */
    println!("");
    find_and_print(String::from("t2"), repo_t2);
}
