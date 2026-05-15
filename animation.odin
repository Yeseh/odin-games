package main

import rl "vendor:raylib"

Animation :: struct {
    texture: rl.Texture2D,
    texture_pixel_size: i32,
    frame_count: i32,
    frame_time: f32,
    frame_current: i32,
    frame_duration: f32
}

init :: proc(
    texture_path: cstring,
    frame_duration: f32
) -> Animation {
    anim := Animation{}
    
    anim.texture = rl.LoadTexture(texture_path)
    anim.texture_pixel_size = 16
    anim.frame_count = anim.texture.width / anim.texture_pixel_size
    anim.frame_time = 0
    anim.frame_current = 0
    anim.frame_duration = frame_duration

    return anim
}

anim_update :: proc(anim: ^Animation) {
    anim.frame_time += rl.GetFrameTime()
    if anim.frame_time >= anim.frame_duration {
        anim.frame_time = 0
        anim.frame_current = (anim.frame_current + 1) % anim.frame_count
    }
}

anim_draw :: proc(
    anim: ^Animation, 
    position: rl.Vector2,
    direction: rl.Vector2,
) {
    anim_frame_offset := f32(anim.frame_current) * f32(anim.texture_pixel_size)

    draw_source := rl.Rectangle{
        x = anim_frame_offset,
        y = 0,
        width = f32(anim.texture_pixel_size) * direction.x,
        height = f32(anim.texture_pixel_size)
    }

    draw_dest := rl.Rectangle{
        x = position.x,
        y = position.y,
        width = f32(anim.texture_pixel_size) * 4 * direction.x,
        height = f32(anim.texture_pixel_size) * 4
    }

    rl.DrawTexturePro(
        anim.texture, 
        draw_source, 
        draw_dest, 0, 0, rl.WHITE)
}

