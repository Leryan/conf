use std::fmt::Debug;

#[derive(Debug)]
enum RepositoryError {
    IOError(String),
}

#[derive(Debug)]
#[allow(dead_code)]
struct BullShit {}

#[derive(Debug)]
struct Type1 {
    pub id: String,
}

#[derive(Debug)]
struct Type2 {
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
    fn find_by_id(&self, id: String) -> Result<Option<T>, RepositoryError> {
        match id.as_str() {
            "found" => return Ok(Some(T::new(String::from("found")))),
            "err" => return Err(RepositoryError::IOError("no connection".to_string())),
            _ => Ok(None),
        }
    }
}

struct GenericRepository<T> {
    phantom: std::marker::PhantomData<T>,
}

impl<T> GenericRepository<T> {
    pub fn new() -> Self {
        return GenericRepository {
            phantom: std::marker::PhantomData,
        };
    }
}

impl<T: Identifiable> Repository<T> for GenericRepository<T> {}

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

    let repo_t1: GenericRepository<Type1> = GenericRepository::new();
    let repo_t2: GenericRepository<Type2> = GenericRepository::new();
    find_and_print(String::from("t1"), repo_t1);
    /* wont build unless implement Copy trait because repo_t1 moved into find_and_print
    repo_t1.find("bla".to_string());
    */
    println!("");
    find_and_print(String::from("t2"), repo_t2);
}
