def is_in_allowed_category(message, category_name="feobot"):
    category = message.channel.category
    return category and category.name.lower() == category_name.lower()
