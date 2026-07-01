from string import Template


top_days_email_template = Template(
"""
<h3>The top 10 days with the most sales are:</h3>
<ul>
    $list_items
</ul>
""")
