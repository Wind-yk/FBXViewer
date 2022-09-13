
# Architecture

The folders and files of this project are organized as follows:

```bash
📦3D
 ┣━📂config # configurations for scripts
 ┃
 ┣━📂data
 ┃ ┣━📂ext  # external 
 ┃ ┣━📂int  # internal
 ┃ ┣━📂med  # intermediate
 ┃ ┗━📂out  # output
 ┃
 ┣━📂docs # documentation
 ┃
 ┣━📂src  # code
 ┃ ┣━📂notebook
 ┃ ┣━📂script
 ┃ ┗━📂packages
 ┃
 ┣━📜README.md
 ┣━📜.gitignore
 ┗━📜environment.yaml
```

![diagram](3D_diagram.jpg)



# The Python environment

A Python environment is a environment such that the Python interpreter, libraries and scripts installed into it are isolated from those installed in other virtual environments. 

Its aim is to ensure that all developers are using the same version of Python and Python libraries, to avoid discrepancies due to different versions.

## Update

If you installed some new packages, remember to refresh the `environment.yaml` using:

```bash
conda env export > environment.yaml
```

If you need to update your environment, use:

```bash
conda env update --f environment.yaml --prune
```
> You can use `--name` to specify the environment to update, as `--name 3D`, otherwise it will update your current environment. The argument `--prune` uninstalls packages that are no longer present in the yaml. 


# How to use git


## Get started

1. In case you have not configured git, follow the instructions at terminal:

    ```bash
    $ git config --global user.name   <github_username>
    $ git config --global user.email  <github_email>
    $ git config --global color.ui    true
    $ git config --global core.editor code
    ```

2. Clone this repo from terminal. This will create the `3D` project folder under your current directory (you may be requested to identify yourself):

    ```bash
    $ git clone https://github.com/Wind-yk/3D
    ```

## Dialy instructions

3. The main instructions and workflow of `git` (Version Control) (information retrieved from https://git-scm.com/docs and  https://atlassian.com/git):
    * Commands
        * To display the state of the working directory and the staging area; to see the tracked, untracked files and changes and to display the state between "git add" and "git commit" command:
            ```bash
            $ git status
            ```
        * To update the index (which contains a snapshot of the content of the working tree) using the current content found in the working tree and to prepare the content staged for the next commit:
            ```bash
            $ git add <file name>
            ```
        * To remove files from the working tree and from the index:
            ```bash
            $ git rm <file name>
            ```
        * To create a new commit containing the current contents of the index:
            ```bash
            $ git commit
            # automatically commit all modified, tracked or deleted files:
            $ git commit -a
            # add a commit message:
            $ git commit -m <message>
            ```
        * To update remote refs along with associated objects; to publish and upload local changes to a central repository; to share the modifications with remote team members:
            ```bash
            $ git push
            ```
        * To list existing branches; the current branch will be highlighted in green and marked with an asterisk:
            ```bash
            $ git branch
            ```
        * To switch branches:
            ```bash
            $ git checkout <branch_name>
            ```
        * To show a list of all the commits made to a repository:
            ```bash
            $ git log
            ```
        * To download commits, files, and refs from a remote repository into the local repositor but isolating that content from existing local content so that it has no effect on the local development work: 
            ```bash
            $ git fetch
            ```
        * To fetch and download content from a remote repository and immediately update the local repository to match that content:
            ```bash
            $ git pull
            ```
        * To reapply commits on top of another base tip; to move or to combine a sequence of commits to a new base commit: 
            ```bash
            $ git rebase
            # In order to restart the rebasing process after having resolved a merge conflict:
            $ git rebase --continue
            ```

    * Workflow

        Definition: It is the definition, execution, and automation of software processes where tasks, information or documents are passed from one program to another for action, according to a set of procedural rules.

        Type: The one implemented in this particular case is the Centralized Workflow, where a central repository is used as the single point-of-entry for all changes to the project.
        (for more information access https://www.atlassian.com/git/tutorials/comparing-workflows#centralized-workflow)

        Functioning (briefly explained): Each developer should first have a local copy of the entire project and they will work on the project as if they were completely isolated. Developers can edit and commit as many times as they wish since these are only local changes; "push" command is used to share the modification with other developers (upload changes to the central repository).

        * How to upload a change to the central repository:

            ```bash
            # (0) save the file locally; (1) add; (2) commit; (3) push
            $ git add <file_name>
            # to include a message or not is optional
            $ git commit -m <message> -m <description>
            $ git push
            ```
            
        * Possible conflicts and how to resolve them:
            
            (A) Push conflict

            If a developer's local commits diverge from the central repository, Git will refuse to push their changes. In other words, if developer A has pushed a new modification on a file when developer B was editing a distinct file, in order to upload the modifications done by B, B should pull first (get the latest version of the project).

            (B) Merge conflict

            If both developers A and B were editing the same file(s) and A has pushed before B, B would have a merge conflict when pushing his/her edit. When encountered this problem, B can  locate these inconsistencies by looking at the "unmerged paths" section after calling the "git status" command. Subsequently, B should manually modify the conflicted file(s), add them, and do rebase; that is:
            ```bash
            $ git add <conflicted_file_name>
            $ git rebase --continue
            ```
            Finally B could successfully push:
            ```bash
            $ git push
            ```
