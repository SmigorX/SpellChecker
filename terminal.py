import asyncio


async def loading_animation(message):
    initial_message = await message.channel.send("```bash\nyay -S dictionary\n```")
    await asyncio.sleep(0.2)

    # Cumulative output variable
    output = "```bash\nyay -S dictionary\nSync Dependency (1): dictionary-5.38.2-1\nwarning: dictionary-5.38.2-1 is up to date -- reinstalling\nresolving dependencies...\nlooking for conflicting packages...\n\nPackages (1) dictionary-5.38.2-1\n\nTotal Installed Size: 69.69 MiB\nNet Upgrade Size: 69.69 MiB\n\n:: Proceed with installation? [Y/n]```"

    # Edit the message to include the initial installation steps
    await initial_message.edit(content=output)
    await asyncio.sleep(0.2)

    # Type 'Y' and simulate delay after typing 'Y'
    updated_output = output.replace(":: Proceed with installation? [Y/n]", ":: Proceed with installation? [Y/n] Y")
    await initial_message.edit(content=updated_output)
    await asyncio.sleep(0.2)

    # Progress bar animation
    progress = 0
    while progress <= 100:
        if progress == 0:
            progress_bar = "[                                                  ]"
        elif progress == 25:
            progress_bar = "[########                                          ] 25%"
        elif progress == 50:
            progress_bar = "[####################                              ] 50%"
        elif progress == 75:
            progress_bar = "[##############################                    ] 75%"
        elif progress == 100:
            progress_bar = "[##################################################] 100% Installation completed successfully!"

        await asyncio.sleep(0.05)  # Adjust sleep time as needed for animation speed
        await initial_message.edit(content=f"```bash\n{progress_bar}\n```")
        progress += 25

    await asyncio.sleep(1)
    await initial_message.edit(content=f"\u200B")

    return initial_message
