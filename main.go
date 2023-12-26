package main

import (
	"os"
	"os/signal"
	"syscall"

	"github.com/bwmarrin/discordgo"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()

	bot, err := discordgo.New("Bot " + os.Getenv("TOKEN"))

	if err != nil {
		panic(err)
	}

	err = bot.Open()

	if err != nil {
		panic(err)
	}

	println("Bot is running!")

	// Slash commands
	commands := []*discordgo.ApplicationCommand{
		{
			Name:        "meme",
			Description: "Get a random meme from reddit",
		},
	}

	registeredCommands := make([]*discordgo.ApplicationCommand, len(commands))
	for i, v := range commands {
		cmd, err := bot.ApplicationCommandCreate(bot.State.User.ID, "", v)

		if err != nil {
			println("Cannot create '%v' command: %v", v.Name, err)
		}

		registeredCommands[i] = cmd
	}

	defer bot.Close()

	sc := make(chan os.Signal, 1)
	signal.Notify(sc, os.Interrupt, syscall.SIGTERM, syscall.SIGINT, syscall.SIGKILL)
	<-sc
}
