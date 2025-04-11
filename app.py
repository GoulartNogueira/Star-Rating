from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

def get_star_rating(rating, size=24, max_stars=5):
    """Get the star rating representation.
    Args:
        rating (float): The rating value between 0 and max_stars.
        size (int): The size of each star in pixels.
        max_stars (int): The maximum number of stars.
    Returns:
        str: An SVG representation of the star rating.
    """
    rating = max(0, min(max_stars, rating))
    full_stars = int(rating)
    partial = rating - full_stars
    empty_stars = max_stars - full_stars - (1 if partial > 0 else 0)
    
    # Using a 0-100 coordinate system for the star path
    star_path = "M50 5L61.5 31.5L90.5 35.5L70 55.5L75.5 84L50 70.5L24.5 84L30 55.5L9.5 35.5L38.5 31.5Z"
    
    star_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 {max_stars * 100} 100" 
        width="{size * max_stars}" 
        height="{size}">'''
    
    # Add full stars
    for i in range(full_stars):
        x = i * 100
        star_svg += f'''
            <path transform="translate({x},0)" fill="gold" d="{star_path}"/>'''
    
    # Add partial star if needed
    if partial > 0:
        x = full_stars * 100
        star_svg += f'''
            <defs>
                <clipPath id="partial">
                    <rect x="0" y="0" width="{partial * 100}" height="100" />
                </clipPath>
            </defs>
            <path transform="translate({x},0)" fill="#ddd" d="{star_path}"/>
            <path transform="translate({x},0)" fill="gold" clip-path="url(#partial)" d="{star_path}"/>'''
    
    # Add empty stars
    for i in range(empty_stars):
        x = (full_stars + (1 if partial > 0 else 0) + i) * 100
        star_svg += f'''
            <path transform="translate({x},0)" fill="#ddd" d="{star_path}"/>'''
    
    star_svg += '</svg>'
    return star_svg


# Moon rating

def get_moon_phase(percentage):
    if percentage <= 0.1:
        return "🌑"  # Empty
    elif percentage <= 0.3:
        return "🌘"  # Waning crescent
    elif percentage <= 0.6:
        return "🌗"  # Half
    elif percentage <= 0.9:
        return "🌖"  # Waxing gibbous
    else:
        return "🌕"  # Full

def get_moon_rating(rating):
    rating = max(min(5, rating), 0)
    output = []
    for i in range(5):
        moon_value = max(0, min(1, rating - i))
        output.append(get_moon_phase(moon_value))
    return ''.join(output)

@app.route('/')
def redirect_to_github():
    return redirect("https://github.com/GoulartNogueira/Star-Rating/", code=302)

@app.route('/<rating>/')
def star_rating(rating):
    try:
        rating = float(rating)
    except ValueError:
        return "Invalid rating value", 400
    
    size = request.args.get('size', default=24, type=int)
    max_stars = request.args.get('max', default=5, type=int)
    svg = get_star_rating(rating, size, max_stars)
    response = make_response(svg)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response

@app.route('/moon/<rating>/')
def moon_rating(rating):
    try:
        rating = float(rating)
    except ValueError:
        return "Invalid rating value", 400
    
    moon_rating_output = get_moon_rating(rating)
    response = make_response(moon_rating_output)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


if __name__ == '__main__':
    path = "http://127.0.0.1:5000"
    print(f"Running on {path}")
    print("Examples:")
    print(f"  {path}/3.5/")
    print(f"  {path}/moon/4.2/")
    print("Press CTRL+C to exit")
    app.run(debug=True)
