import { z } from "zod";

export const env = z
  .object({
    MONGO_URI: z.string(),
    MONGO_DB: z.string(),
  })
  .parse(process.env);
