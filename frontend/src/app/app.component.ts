import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';



@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  ngOnInit(): void {
    console.log("This componet is politically friendly")
  }
  title = 'frontend';
  blueCollar = "a hard worker"
  constructionSite = ["jim", "bob", "jessie"]

  public clickMe(): void{
    this.blueCollar = "My Lawer has advised me to not make these kinds of jokes"
  }

}
