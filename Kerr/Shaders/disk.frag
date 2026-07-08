#version 330

in vec3 worldPos;
in vec2 diskUV;
in vec4 vertexColor;
in float radius;

uniform float time;

out vec4 fragColor;

//====================================================
// Noise
//====================================================

float hash(vec2 p)
{
    return fract(sin(dot(p, vec2(41.0,289.0))) * 43758.5453);
}

float noise(vec2 p)
{
    vec2 i=floor(p);
    vec2 f=fract(p);

    float a=hash(i);
    float b=hash(i+vec2(1,0));
    float c=hash(i+vec2(0,1));
    float d=hash(i+vec2(1,1));

    vec2 u=f*f*(3.0-2.0*f);

    return mix(a,b,u.x)
        +(c-a)*u.y*(1.0-u.x)
        +(d-b)*u.x*u.y;
}

// Gradient noise variant to break up hash grid artefacts
float gnoise(vec2 p)
{
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f*f*(3.0-2.0*f);

    vec2 ga = vec2(hash(i)*2.0-1.0, hash(i+vec2(3.7,1.1))*2.0-1.0);
    vec2 gb = vec2(hash(i+vec2(1,0))*2.0-1.0, hash(i+vec2(1,0)+vec2(3.7,1.1))*2.0-1.0);
    vec2 gc = vec2(hash(i+vec2(0,1))*2.0-1.0, hash(i+vec2(0,1)+vec2(3.7,1.1))*2.0-1.0);
    vec2 gd = vec2(hash(i+vec2(1,1))*2.0-1.0, hash(i+vec2(1,1)+vec2(3.7,1.1))*2.0-1.0);

    float va = dot(ga, f);
    float vb = dot(gb, f - vec2(1,0));
    float vc = dot(gc, f - vec2(0,1));
    float vd = dot(gd, f - vec2(1,1));

    return 0.5 + 0.5*(mix(mix(va,vb,u.x), mix(vc,vd,u.x), u.y));
}

float fbm(vec2 p)
{
    float v=0.0;
    float a=0.5;

    // Rotated octaves to break up grid repetition
    mat2 rot = mat2(cos(0.5), -sin(0.5), sin(0.5), cos(0.5));

    for(int i=0;i<6;i++)
    {
        v+=a*gnoise(p);
        p = rot * p * 2.03;
        a*=0.5;
    }

    return v;
}

//====================================================

void main()
{
    float angle = atan(diskUV.y,diskUV.x);

    //------------------------------------------------
    // Inner radius for colour gradient (ISCO ~ 2.3)
    //------------------------------------------------

    float r_inner = 2.3;
    float r_outer = 7.0;

    // t = 0 at innermost edge, 1 at outermost
    float t = clamp((radius - r_inner) / (r_outer - r_inner), 0.0, 1.0);

    //------------------------------------------------
    // Doppler
    //------------------------------------------------

    vec2 orbitDir = normalize(vec2(-diskUV.y,diskUV.x));
    vec2 viewDir = normalize(vec2(0.0,-1.0));

    float doppler = dot(orbitDir,viewDir);
    float dopplerFactor = doppler*0.5+0.5;

    float boost = mix(
        0.75,
        1.20,
        dopplerFactor
    );

    //------------------------------------------------
    // Domain Warp — polar-space to avoid tiling
    // Use angle + radius as the base coords so the
    // noise lives in a continuous cylinder, not a
    // repeating 2-D grid.
    //------------------------------------------------

    // Polar base: angle wraps continuously, radius scales smoothly
    vec2 polar = vec2(angle * 1.2 + time * 0.08, radius * 0.55 - time * 0.06);

    // First warp pass
    vec2 warp = polar + vec2(
        fbm(polar + vec2(1.7, 9.2)),
        fbm(polar + vec2(8.3, 2.8))
    ) * 0.7;

    // Second (finer) warp pass
    vec2 flow = warp + vec2(
        fbm(warp * 1.8 + time * 0.18),
        fbm(warp * 1.8 - time * 0.14)
    ) * 0.35;

    //------------------------------------------------
    // Plasma
    //------------------------------------------------

    float plasma =
        fbm(flow * 3.5);

    plasma +=
        fbm(flow * 7.0 + vec2(time*0.1, -time*0.07)) * 0.40;

    plasma +=
        fbm(flow * 15.0) * 0.15;

    // Normalise to [0,1]
    plasma = clamp(plasma, 0.0, 1.0);

    //------------------------------------------------
    // Spiral Arms — modulated, not dominant
    //------------------------------------------------

    float spiral =
        sin(
            angle*20.0
            - radius*7.0
            - time*2.8
            + plasma*5.0
        );

    spiral = smoothstep(-0.3, 1.0, spiral) * 0.6;

    //------------------------------------------------
    // Heat — only white at the very inner edge
    // Use a steep falloff so 70 % of disk is NOT white
    //------------------------------------------------

    // heat = 1.0 right at inner edge, falls off quickly
    float heat = exp(-t * 3.8);          // was exp(-radius*0.45) which stayed high too long

    //------------------------------------------------
    // Physical Colour Gradient
    // white → yellow → orange → dark red
    // mapped directly to t (radial position)
    //------------------------------------------------

    // 4-stop gradient across the disk
    vec3 col_white  = vec3(1.00, 0.98, 0.90);   // t=0  (innermost)
    vec3 col_yellow = vec3(1.00, 0.80, 0.20);   // t=0.2
    vec3 col_orange = vec3(0.95, 0.35, 0.04);   // t=0.5
    vec3 col_dkred  = vec3(0.48, 0.06, 0.01);   // t=1  (outermost)

    vec3 colour;
    if (t < 0.20) {
        colour = mix(col_white,  col_yellow, t / 0.20);
    } else if (t < 0.50) {
        colour = mix(col_yellow, col_orange, (t - 0.20) / 0.30);
    } else {
        colour = mix(col_orange, col_dkred,  (t - 0.50) / 0.50);
    }

    // Plasma adds brightness variation but doesn't recolour everything white
    colour = mix(colour, colour * 1.45, plasma * 0.55);

    // Spiral arms contribute a mild brightness band, not colour override
    colour *= (0.75 + spiral * 0.25);

    //------------------------------------------------
    // Density (brightness variation from plasma)
    //------------------------------------------------

    float density =
        smoothstep(
            0.20,
            1.0,
            plasma
        );

    colour *=
        mix(
            0.70,
            1.20,
            density
        );

    //------------------------------------------------
    // Orbiting Hotspots — kept, but dimmer
    //------------------------------------------------

    float hotspot =
        fbm(
            flow * 12.0 +
            vec2(
                time * 1.2,
                -time * 0.8
            )
        );

    hotspot =
        smoothstep(
            0.80,
            0.96,
            hotspot
        );

    // Hotspots only appear on inner (hot) part of disk
    colour +=
        hotspot
        * heat
        * vec3(1.20, 0.90, 0.55)
        * 0.45;

    //------------------------------------------------
    // Vertical Thickness
    //------------------------------------------------

    float vertical =
        exp(
            -abs(worldPos.y)*6.5
        );

    colour *= vertical;

    //------------------------------------------------
    // Glow — much more restrained than before
    // Old: 0.55 + heat*2.0 → saturated everything white
    //------------------------------------------------

    float glow =
        0.45
        + heat * 0.85       // was 2.0 — the main culprit
        + plasma * 0.15;    // was 0.25

    colour *= glow;

    //------------------------------------------------
    // Doppler
    //------------------------------------------------

    colour *= boost;

    vec3 blueShift =
        vec3(
            0.93,
            0.97,
            1.12
        );

    vec3 redShift =
        vec3(
            1.12,
            0.92,
            0.74
        );

    colour =
        mix(
            colour*redShift,
            colour*blueShift,
            dopplerFactor
        );

    //------------------------------------------------
    // Rim Glow — toned down to avoid washing out colour
    //------------------------------------------------

    float rim =
        pow(
            1.0-
            abs(worldPos.y),
            5.0
        );

    colour +=
        vec3(
            0.90,
            0.55,
            0.18
        )
        *rim
        *0.30;   // was 0.7

    //------------------------------------------------
    // Alpha
    //------------------------------------------------

    float alpha =
        smoothstep(
            6.4,
            5.3,
            radius
        );

    //------------------------------------------------
    // ACES Filmic Tone Mapping
    // With lower pre-tone-map values the ACES curve will
    // no longer clip everything to white.
    //------------------------------------------------

    colour =
        (colour * (2.51 * colour + 0.03))
        /
        (colour * (2.43 * colour + 0.59) + 0.14);

    colour = clamp(
        colour,
        0.0,
        1.0
    );

    // Gamma

    colour = pow(
        colour,
        vec3(1.0 / 2.2)
    );

    fragColor =
        vec4(
            colour,
            alpha
        );
}