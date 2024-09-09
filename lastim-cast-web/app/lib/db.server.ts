import { MongoClient } from "mongodb";
import { env } from "./env.server";

export const createDbConnection = async () => {
  const client = new MongoClient(env.MONGO_URI);
  await client.connect();

  return client.db(env.MONGO_DB);
};
