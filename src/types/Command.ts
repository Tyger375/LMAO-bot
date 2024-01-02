import {
  ApplicationCommandOptionData,
  Client,
  CommandInteraction,
} from "discord.js";

type Command = {
  name: string;
  description: string;
  options?: ApplicationCommandOptionData[];
  execute: (interaction: CommandInteraction, client: Client) => Promise<void>;
};

export type { Command };
