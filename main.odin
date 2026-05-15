package main

import rl "vendor:raylib"

main :: proc() {

    WIN_HEIGHT :: 720
    WIN_WIDTH :: 1280

    rl.InitWindow(WIN_WIDTH, WIN_HEIGHT, "Hello Raylib in Odin")
    defer rl.CloseWindow()

    gravity:f32 = 2000

    player_size := rl.Vector2{64, 64}
    player_pos := rl.Vector2{640, 320}
    player_speed: f32 = 400 
    player_vel : rl.Vector2
    player_grounded := false
    player_direction := rl.Vector2{1, 0} 

    player_run_texture := rl.LoadTexture("sprites/dog_walk.png")
    player_run_width := f32(player_run_texture.width) 
    player_run_height := f32(player_run_texture.height) 
    player_run_frames := 4
    player_run_frame_time: f32
    player_run_frame_current: int 
    player_run_frame_duration := f32(0.1)
    
    for !rl.WindowShouldClose() {
        rl.BeginDrawing()
        defer rl.EndDrawing()

        rl.ClearBackground(rl.BLUE)

        rl.DrawRectangleV(
            {0, f32(rl.GetScreenHeight()) - 64.0},
            {f32(rl.GetScreenWidth()), 64.0},
            rl.GRAY
        )

        if rl.IsKeyDown(.A) {
            player_vel.x = -player_speed 
            player_direction = rl.Vector2{-1, 0}
        }
        else if rl.IsKeyDown(.D) {
            player_vel.x = player_speed 
            player_direction = rl.Vector2{1, 0}
        }
        else {
            player_vel.x = 0 
        }

        if player_grounded && rl.IsKeyPressed(.BACKSPACE) {
            player_vel.y = -500
            player_grounded = false
        }

        if player_pos.y > f32(rl.GetScreenHeight()) - 64*2 {
            player_pos.y = f32(rl.GetScreenHeight()) - 64*2
            player_grounded = true
        }

        if player_pos.x < 0 {
            diff := f32(player_pos.x)   
            player_pos.x = f32(rl.GetScreenWidth()) - player_pos.x 
        }
        else if player_pos.x > f32(rl.GetScreenWidth()) {
            diff := f32(player_pos.x) - f32(rl.GetScreenWidth())
            player_pos.x = 0 + diff
        }

        player_vel.y += gravity * rl.GetFrameTime()
        player_pos += player_vel * rl.GetFrameTime() 

        player_run_frame_time += rl.GetFrameTime()
        if player_run_frame_time > player_run_frame_duration {
            player_run_frame_current = (player_run_frame_current + 1) % player_run_frames
            player_run_frame_time = 0
        }

        draw_player_offset_x := f32(player_run_frame_current) * (player_run_width / f32(player_run_frames))
        draw_player_source := rl.Rectangle{
            x = draw_player_offset_x,
            y = 0,
            width = player_run_width / f32(player_run_frames) * player_direction.x,
            height = player_run_height
        }

        draw_player_dest := rl.Rectangle{
            x = player_pos.x,
            y = player_pos.y,
            width = player_run_width * 4 / f32(player_run_frames), 
            height = player_run_height * 4 
        }

        rl.DrawTexturePro(
            player_run_texture, 
            draw_player_source, 
            draw_player_dest, 0, 0, rl.WHITE)
    }
}