var conn;
try
{
    conn = new Mongo("localhost:27017");
}
catch(Error)
{
    //print(Error);
}
while(conn===undefined)
{
    try
    {
        conn = new Mongo("localhost:27017");
    }
    catch(Error)
    {
        //print(Error);
    }
    sleep(30);
}
DB = conn.getDB("newsblaster");
Result = DB.runCommand('buildInfo');
print(Result.version);
