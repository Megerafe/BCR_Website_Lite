/**
 * Returns the items of a list collection (services, packages, portfolio, faq)
 * in the SAME order as they are written in the YAML file.
 */
import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';
import { getCollection } from 'astro:content';

type ListCollection = 'services' | 'packages' | 'portfolio' | 'faq';

function yamlOrder(name: ListCollection): string[] {
  const file = path.resolve(process.cwd(), `src/content/${name}.yaml`);
  const data = (parse(fs.readFileSync(file, 'utf8')) ?? []) as { id: string }[];
  return data.map((d) => String(d.id));
}

export async function getOrdered<C extends ListCollection>(name: C) {
  const items = await getCollection(name);
  const order = yamlOrder(name);
  return items.sort((a, b) => order.indexOf(a.id) - order.indexOf(b.id));
}
