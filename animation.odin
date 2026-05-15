package main

import rl "vendor:raylib"

AnimatedSprite :: struct {
    texture: rl.Texture2D,
    frame_count: int,
    frame_time: f32,
    frame_current: int,
    frame_duration: f32
}

init :: proc(
    texture_path: cstring,
    frame_duration: f32
) -> AnimatedSprite {
    anim := AnimatedSprite{}
    
    anim.texture = rl.LoadTexture(texture_path)
    anim.frame_count = int(anim.texture.width / 16)
    anim.frame_time = 0
    anim.frame_current = 0
    anim.frame_duration = 0.1

    return anim
}

anim_get_draw_rects :: proc(
    anim: ^AnimatedSprite, 
    position: rl.Vector2,
    direction: rl.Vector2,
) -> (rl.Rectangle, rl.Rectangle) {
    draw_player_offset_x := f32(anim.frame_current) * 16.0
    draw_source := rl.Rectangle{
        x = draw_player_offset_x,
        y = 0,
        width = 16.0 * direction.x,
        height = 16.0
    }
    draw_dest := rl.Rectangle{
        x = position.x,
        y = position.y,
        width = 64.0 * direction.x,
        height = 64.0
    }
    return draw_source, draw_dest
}

