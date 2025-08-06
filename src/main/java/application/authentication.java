package application;

import org.bson.Document;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class authentication {
  private static final String MONGO_URI = System.getenv("mongo_auth");
  
  public static boolean AuthToken(String inTocken) {
    try (MongoClient mongoClient = MongoClients.create(MONGO_URI)){
      MongoDatabase database = mongoClient.getDatabase("ApiKey");
      MongoCollection<Document> collection = database.getCollection("token");

      Document query = new Document("key", inTocken);
      Document result = collection.find(query).first();

      return result != null; 
    }
    catch (Exception e) {
      e.printStackTrace();
      return false;
    }
  } 
}