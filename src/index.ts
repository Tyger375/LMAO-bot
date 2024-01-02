import type { Command } from "./types/Command";
import { Client, GatewayIntentBits } from "discord.js";
import { consola } from "consola";
import fs from "fs";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.on("ready", async () => {
  consola.success(`Logged in as ${client.user?.tag}`);

  consola.info("Registering commands...");

  const commands = fs
    .readdirSync(process.env.PRODUCTION ? "./dist/commands" : "./src/commands")
    .filter((file) => file.endsWith(process.env.PRODUCTION ? ".js" : ".ts"));

  for (const command of commands) {
    const { default: cmd } = (await import(`./commands/${command}`)) as {
      default: Command;
    };

    consola.info(`Registering /${cmd.name}...`);

    client.application.commands.create({
      name: cmd.name,
      description: cmd.description,
      options: cmd.options || [],
    });
  }

  consola.success("Registered commands successfully");
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isCommand()) return;

  let commands: Command[] = [];

  // Save the commands to a variable so we don't have to read the directory every time
  if (commands.length === 0) {
    const list = fs.readdirSync(
      process.env.PRODUCTION ? "./dist/commands" : "./src/commands",
    ).filter((file) => file.endsWith(process.env.PRODUCTION ? ".js" : ".ts"));

    for (const command of list) {
      const { default: cmd } = (await import(`./commands/${command}`)) as {
        default: Command;
      };

      commands.push(cmd);
    }

    consola.info("Cached commands successfully");
  }

  if (!commands.some((cmd) => interaction.commandName === cmd.name)) return;

  const cmd = commands.find((cmd) => interaction.commandName === cmd.name);

  if (!cmd) return;

  await cmd.execute(interaction, client);
});

client.login(process.env.TOKEN);
