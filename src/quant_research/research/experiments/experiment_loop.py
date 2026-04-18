class ExperimentLoop:

    def __init__(self, runner):
        self.runner = runner

    def run(self, configs: list):

        results = []

        for i, config in enumerate(configs):

            print(f"\n--- Running experiment {i+1}/{len(configs)} ---")

            try:
                result = self.runner.run(config)
                results.append(result)

            except Exception as e:
                print(f"Failed: {e}")

        return results