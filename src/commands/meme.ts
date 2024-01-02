import axios from "axios";
import type { Command } from "../types/Command";
import { RandomMeme } from "../types/Reddit";

export default {
  name: "meme",
  description: "Get a random meme from Reddit",
  async execute(interaction, _) {
    const response = await axios<RandomMeme>({
      method: "GET",
      url: "https://www.reddit.com/r/memes/random/.json",
      headers: {
        "User-Agent": "curl/7.77.0",
      },
    });

    const url = response.data[0].data.children[0].data.url_overridden_by_dest;
    const title = response.data[0].data.children[0].data.title;
    const author = response.data[0].data.children[0].data.author;
    const subreddit = response.data[0].data.children[0].data.subreddit;
    const permalink = response.data[0].data.children[0].data.permalink;

    await interaction.reply({
      embeds: [
        {
          title: title,
          url: `https://reddit.com${permalink}`,
          image: {
            url: url,
          },
          footer: {
            text: `Posted by u/${author} on r/${subreddit}`,
          }
        }
      ],
    });
  },
} as Command;
