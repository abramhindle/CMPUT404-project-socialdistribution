import Author from "./models/Author";

declare global {
  namespace Express {
    export interface Request {
      authorId?: Author["id"];
    }
  }
}
