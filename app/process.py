def score_product(product, user_preferences):
    # Define scoring system
    cost_scores = {'£300': 1, '£400': 2, '£500': 3}
    build_quality_scores = {'plastic': 1, 'metal': 2, 'glass': 3}
    performance_scores = {'8GB': 1, '16GB': 2, '32GB': 3}

    # Calculate scores for each category
    cost_score = cost_scores[product['price']]
    build_quality_score = build_quality_scores[product['material']]
    performance_score = performance_scores[product['ram']]

    # Adjust weight factors based on user preferences
    weight_factors = {
        'cost': user_preferences['cost'], 'build quality': user_preferences['build quality'], 'performance': user_preferences['performance']}

    # Calculate total score
    total_score = (cost_score * weight_factors['cost'] +
                   build_quality_score * weight_factors['build quality'] +
                   performance_score * weight_factors['performance'])

    return total_score


# Example usage
product = {'price': '£300', 'screenSize': '13inch',
           'material': 'plastic', 'ram': '16GB'}
# These values should be collected from the user
user_preferences = {'cost': 0.5, 'build quality': 0.3, 'performance': 0.2}
print(score_product(product, user_preferences))
