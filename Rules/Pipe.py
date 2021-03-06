class Pipe:

    @staticmethod
    def run(raw_contents, rules_list):
        leads = []
        for content in raw_contents:
            if content.author is None:  # User was deleted
                continue
            for rule in rules_list:
                lead = rule.execute_rule(content)
                if lead is not None:
                    leads.append(lead)
        return leads
