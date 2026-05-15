package main

import rl "vendor:raylib"

PlayerAnimationState :: enum {
    Idle,
    Run,
    Jumping
}

Player :: struct {
    pos: rl.Vector2,
    vel: rl.Vector2,
    speed: f32,
    grounded: bool,
    direction: rl.Vector2,
    state: PlayerAnimationState,
}

WIN_HEIGHT :: 720
WIN_WIDTH  :: 1280

player := Player{
    pos = rl.Vector2{640, 320},
    vel = rl.Vector2{0, 0},
    speed = 300,
    grounded = false,
    direction = rl.Vector2{1, 0},
    state = .Idle
}

gravity: f32 = 2000

main :: proc() {
    rl.InitWindow(WIN_WIDTH, WIN_HEIGHT, "Hello Raylib in Odin")
    defer rl.CloseWindow()

    player_anim_run : AnimatedSprite = init("sprites/dog_walk.png", 0.1)
    player_anim_idle : AnimatedSprite = init("sprites/dog_idle.png", 0.1)

    for !rl.WindowShouldClose() {
        update(&player)

        rl.BeginDrawing()
        defer rl.EndDrawing()

        rl.ClearBackground(rl.BLUE)

        rl.DrawRectangleV(
            {0, f32(rl.GetScreenHeight()) - 64.0},
            {f32(rl.GetScreenWidth()), 64.0},
            rl.GRAY
        )

        player_active_anim : ^AnimatedSprite = {}
        switch player.state {
        case .Idle:
            player_active_anim = &player_anim_idle
        case .Run:
            player_active_anim = &player_anim_run
        case .Jumping:
            player_active_anim = &player_anim_idle
        }

        player_active_anim.frame_time += rl.GetFrameTime()
        if player_active_anim.frame_time > player_active_anim.frame_duration {
            player_active_anim.frame_current = (player_active_anim.frame_current + 1) % player_active_anim.frame_count
            player_active_anim.frame_time = 0
        }

        draw_source, draw_dest := anim_get_draw_rects(player_active_anim, player.pos, player.direction)
        rl.DrawTexturePro(
            player_active_anim.texture, 
            draw_source, 
            draw_dest, 0, 0, rl.WHITE)
    }
}

update :: proc(player: ^Player) {
    if player.pos.x < 0 {
        diff := f32(player.pos.x)   
        player.pos.x = f32(rl.GetScreenWidth()) - player.pos.x 
    }
    else if player.pos.x > f32(rl.GetScreenWidth()) {
        diff := f32(player.pos.x) - f32(rl.GetScreenWidth())
        player.pos.x = 0 + diff
    }

    if rl.IsKeyDown(.A) {
        player.vel.x = -player.speed 
        player.direction = rl.Vector2{-1, 0}
        player.state = .Run
    }
    else if rl.IsKeyDown(.D) {
        player.vel.x = player.speed 
        player.direction = rl.Vector2{1, 0}
        player.state = .Run
    }
    else {
        player.vel.x = 0 
        player.state = .Idle
    }

    if player.grounded && rl.IsKeyPressed(.BACKSPACE) {
        player.vel.y = -500
        player.grounded = false
    }


    if player.pos.y > f32(rl.GetScreenHeight()) - 64*2 {
        player.pos.y = f32(rl.GetScreenHeight()) - 64*2
        player.grounded = true
    }

    player.vel.y += gravity * rl.GetFrameTime()
    player.pos += player.vel * rl.GetFrameTime()
}
