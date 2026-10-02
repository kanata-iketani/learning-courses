variable "node_count" {
  default = 4
}

# count = 変数 で個数を外から差し替えられるようにするのが実務の形です。
# count.index は 0 始まりなので、そのまま使うと node-0 〜 node-3 になります。
resource "terraform_data" "node" {
  count = var.node_count
  input = format("node-%d", count.index)
}

output "all_nodes" {
  value = join(",", terraform_data.node[*].output)
}

output "last" {
  value = terraform_data.node[3].output
}

output "total" {
  value = length(terraform_data.node)
}
