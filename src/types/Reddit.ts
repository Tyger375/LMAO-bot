export interface RandomMeme {
  kind: string;
  data: {
    after: string | null;
    dist: number;
    modhash: string;
    geo_filter: string | null;
    children: {
      kind: string;
      data: {
        title: string;
        subreddit: string;
        permalink: string;
        author: string;
        thumbnail: string;
        url_overridden_by_dest: string;
      }
    }[];
  }
}
