export default interface Post {
  id: string;
  title: string;
  source: string;
  origin: string;
  description: string;
  contentType:
    | "text/markdown"
    | "text/plain"
    | "application/base64"
    | "image/png;base64"
    | "image/jpeg;base64";
  content: string;
  image: string;
  categories: string[];
  count: number;
  published: Date;
  visibility: "PUBLIC" | "FRIENDS";
  unlisted: boolean;
}
