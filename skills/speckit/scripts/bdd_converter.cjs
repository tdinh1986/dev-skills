const fs = require('fs');

/**
 * script: bdd_converter.cjs
 * description: Converts structured JSON requirements into standard Gherkin/BDD format.
 * usage: node bdd_converter.cjs '<json_string>'
 */

function formatBDD(input) {
  let data;
  try {
    data = typeof input === 'string' ? JSON.parse(input) : input;
  } catch (e) {
    return "Error: Invalid JSON input.";
  }

  if (!data.feature || !data.scenarios || !Array.isArray(data.scenarios)) {
    return "Error: Input must contain 'feature' (string) and 'scenarios' (array).";
  }

  let output = `Feature: ${data.feature}\n`;

  data.scenarios.forEach(scenario => {
    output += `\n  Scenario: ${scenario.title}\n`;
    
    if (scenario.given && scenario.given.length > 0) {
      output += `    Given ${scenario.given[0]}\n`;
      scenario.given.slice(1).forEach(line => output += `    And ${line}\n`);
    }
    
    if (scenario.when && scenario.when.length > 0) {
      output += `    When ${scenario.when[0]}\n`;
      scenario.when.slice(1).forEach(line => output += `    And ${line}\n`);
    }
    
    if (scenario.then && scenario.then.length > 0) {
      output += `    Then ${scenario.then[0]}\n`;
      scenario.then.slice(1).forEach(line => output += `    And ${line}\n`);
    }
  });

  return output;
}

// CLI Handler
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Please provide a JSON string as an argument.");
    process.exit(1);
  }
  console.log(formatBDD(args[0]));
}

module.exports = formatBDD;
