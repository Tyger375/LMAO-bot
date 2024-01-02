import type { Command } from "../types/Command";

export default {
  name: "8ball",
  description: "Helps you make decisions",
  options: [
    {
      name: "question",
      description: "The question you want to ask",
      type: 3,
      required: true,
    }
  ],
  async execute(interaction, _) {
    const question = interaction.options.get("question");

    const replies = [
      "It is certain",
      "I think so",
      "Nah, I don't think so",
      "Not sure",
      "Definitely",
      "Nope",
    ];

    const choise = replies[Math.floor(Math.random() * replies.length)];

    await interaction.reply({
      content: `🎱 ${question.value}: ${choise}`,
    });
  },
} as Command;
