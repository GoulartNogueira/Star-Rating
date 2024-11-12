from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

def get_star_rating(rating, size=24):
    """Get the star rating representation.
    Args:
        rating (float): The rating value between 0 and 5.
        size (int): The size of each star in pixels.
    Returns:
        str: An SVG representation of the star rating.
    """
    rating = max(0, min(5, rating))
    full_stars = int(rating)
    partial = rating - full_stars
    empty_stars = 5 - full_stars - (1 if partial > 0 else 0)
    
    # Using a 0-100 coordinate system for the star path
    star_path = "M50 5L61.5 31.5L90.5 35.5L70 55.5L75.5 84L50 70.5L24.5 84L30 55.5L9.5 35.5L38.5 31.5Z"
    
    star_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 500 100" 
        width="{size * 5}" 
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
    svg = get_star_rating(rating, size)
    response = make_response(svg)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response

if __name__ == '__main__':
    app.run(debug=True)