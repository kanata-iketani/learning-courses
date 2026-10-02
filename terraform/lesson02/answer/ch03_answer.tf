# server の input に network の output を参照で渡すと、
# 「network を先に作る」という依存関係が自動でできます(順序指定は不要)。
resource "terraform_data" "network" {
  input = "vpc-main"
}

resource "terraform_data" "server" {
  input = terraform_data.network.output
}

output "network_name" {
  value = terraform_data.network.output
}

output "server_network" {
  value = terraform_data.server.output
}
