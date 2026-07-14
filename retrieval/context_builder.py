def build_context(evidence):

    context = "\n".join(
        f"- {item}"
        for item in evidence
    )

    return context