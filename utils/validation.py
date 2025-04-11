import logging

logger = logging.getLogger(__name__)

def validate_dataset(df, rules=None):
    if rules is None:
        rules = get_default_validation_rules()

    validation_issues = []
    rows_before = len(df)

    for rule in rules:
        rule_name = rule.get('name', 'unnamed_rule')
        condition = rule['condition']
        action = rule.get('action', 'report')

        issue_mask = ~condition(df)
        issue_count = issue_mask.sum()

        if issue_count > 0:
            logger.warning(f"Validation rule '{rule_name}' found {issue_count} issues.")
            validation_issues.append({
                'rule_name': rule_name,
                'issue_count': issue_count,
                'percentage': round(issue_count / len(df) * 100, 2)
            })

            # Take action based on rule configuratoin
            if action == 'remove':
                df = df[~issue_mask]
            elif action == 'fix' and 'fix_function' in rule:
                df = rule['fix_function'](df, issue_mask)

    rows_after = len(df)
    logger.info(f"Rows before validation: {rows_before}, Rows after validation: {rows_after}")
    return df, validation_issues                


def get_default_validation_rules():
    return [
        {
            'name': 'price_reasonable_range',
            'condition': lambda df: (df['price'] >= 100000) & (df['price'] <= 10000000),
            'action': 'remove',
        },
        {
            'name': 'area_reasonable_range',
            'condition': lambda df: (df['area_sqm'] >= 10) & (df['area_sqm'] <= 3000),
            'action': 'remove',
        },
        {
            'name': 'price_per_sqm_reasonable',
            'condition': lambda df: (df['price_per_sqm'] >= 1000) & (df['price_per_sqm'] <= 50000),
            'action': 'fix',
            'fix_function': lambda df, mask: df.assign(price_per_sqm=lambda x: x['price_per_sqm'].mask(mask, x['price'] / x['area_sqm']))
        }
    ]        